from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver
from colab.plugins import helpers
from colab.accounts.models import User
from pydiscourse.sso import sso_validate, sso_redirect_url
import requests
import re

def perform_discourse_login(user):
    plugin_config = helpers.get_plugin_config('colab_discourse')
    prefix = helpers.get_plugin_prefix('colab_discourse', regex=False)
    domain = Site.objects.get_current().domain
    base_url = "%s/%s" % (domain, prefix)
    url = base_url + "/session/sso"

    response = requests.get(url, allow_redirects=False)
    if response.status_code == 302:
        location = response.headers.get("Location")

        regex = re.compile(r"sso=(.+)&sig=(.+)")
        matches = regex.search(location)
        payload, signature = matches.groups()
        secret = plugin_config.get('sso_secret')

        nonce = sso_validate(payload, signature, secret)
        if user.profile.avatar:
            url = sso_redirect_url(nonce, secret, user.email,
                                   user.id, user.username,
                                   avatar_url=domain + user.profile.get_avatar_140x140(),
                                   avatar_force_update=True)
        else:
            url = sso_redirect_url(nonce, secret, user.email, user.id, user.username)
        response = requests.get(base_url + url, allow_redirects=False)
        return response
    return None

def login_user(sender, user, request, **kwargs):
    response = perform_discourse_login(user)
    if response:
        session = response.cookies.get('_forum_session')
        t_cookie = response.cookies.get('_t')
        request.COOKIES.set("_forum_session", session)
        request.COOKIES.set("_t", t_cookie)


def logout_user(sender, user, request, **kwargs):
    request.COOKIES.delete('_forum_session')
    request.COOKIES.delete('_t')


@receiver(post_save, sender=User)
def create_discourse_accounts(sender, instance, **kwargs):
    if instance.is_active:
        perform_discourse_login(instance)
