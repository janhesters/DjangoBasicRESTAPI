from allauth.socialaccount.providers.facebook.views import \
    FacebookOAuth2Adapter
from rest_auth.registration.views import SocialConnectView, SocialLoginView


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class FacebookConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter
