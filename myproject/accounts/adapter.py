from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.utils import build_absolute_uri
from django.http import HttpResponseRedirect
from django.urls import reverse


class CustomAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url."""
        url = reverse(
            "accounts:account_confirm_email",
            args=[emailconfirmation.key]
        )
        ret = build_absolute_uri(
            request,
            url
        )
        return ret

    def get_email_confirmation_redirect_url(self, request):
        """
        The URL to return to after successful e-mail confirmation.
        """
        url = reverse(
            "accounts:email_activation_done"
        )
        ret = build_absolute_uri(
            request,
            url
        )
        return ret

    def respond_email_verification_sent(self, request, user):
        return HttpResponseRedirect(
            reverse('accounts:account_email_verification_sent')
        )


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        """
        Returns the default URL to redirect to after successfully
        connecting a social account.
        """
        assert request.user.is_authenticated
        url = reverse('accounts:socialaccount_connections')
        return url
