from django.contrib.auth import views
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _


class CustomPasswordResetConfirmView(views.PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")
    template_name = "registration/password_reset_confirm.html"


class CustomPasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"


def email_activation_done(request):
    return HttpResponse(_('Thank you for your email confirmation. You can now use your account.'))


def account_email_verification_sent(request):
    return HttpResponse(_('Thank you for your registration. An email with an activation link has been send.'))
