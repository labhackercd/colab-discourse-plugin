from django.conf import settings
from colab.plugins import helpers
from pydiscourse.sso import sso_validate, sso_redirect_url
import requests
import re


def login_user(sender, user, request, **kwargs):
    base_url = request.build_absolute_uri().replace(request.path, "/")
    base_url += helpers.get_plugin_prefix('colab_discourse', regex=False)
    url = base_url + "/session/sso"

    response = requests.get(url, allow_redirects=False)
    if response.status_code != 502:
        location = response.headers.get("Location")

        regex = re.compile(r"sso=(.+)&sig=(.+)")
        matches = regex.search(location)
        payload, signature = matches.groups()
        secret = settings.DISCOURSE_SSO_SECRET

        nonce = sso_validate(payload, signature, secret)
        url = sso_redirect_url(nonce, secret, user.email,
                               user.id, user.username)
        response = requests.get(base_url + url, allow_redirects=False)
        session = response.cookies.get('_forum_session')
        t_cookie = response.cookies.get('_t')
        request.COOKIES.set("_forum_session", session)
        request.COOKIES.set("_t", t_cookie)


def logout_user(sender, user, request, **kwargs):
    pass
