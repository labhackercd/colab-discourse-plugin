from colab.plugins import helpers
from pydiscourse.sso import sso_validate, sso_redirect_url
import requests
import re


def login_user(sender, user, request, **kwargs):
    plugin_config = helpers.get_plugin_config('colab_discourse')
    request_path_regex = "{}.*".format(request.path)
    base_url = request.build_absolute_uri()
    base_url = re.sub(request_path_regex, '/', base_url)
    base_url += helpers.get_plugin_prefix('colab_discourse', regex=False)
    url = base_url + "/session/sso"

    response = requests.get(url, allow_redirects=False)
    if response.status_code == 302:
        location = response.headers.get("Location")

        regex = re.compile(r"sso=(.+)&sig=(.+)")
        matches = regex.search(location)
        payload, signature = matches.groups()
        secret = plugin_config.get('sso_secret')

        nonce = sso_validate(payload, signature, secret)
        url = sso_redirect_url(nonce, secret, user.email,
                               user.id, user.username)
        response = requests.get(base_url + url, allow_redirects=False)
        session = response.cookies.get('_forum_session')
        t_cookie = response.cookies.get('_t')
        request.COOKIES.set("_forum_session", session)
        request.COOKIES.set("_t", t_cookie)


def logout_user(sender, user, request, **kwargs):
    request.COOKIES.delete('_forum_session')
    request.COOKIES.delete('_t')
