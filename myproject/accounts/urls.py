from allauth.account import views as allauth_views
from allauth.socialaccount import views as allauth_social_views
from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r"^confirm-email/(?P<key>[-:\w]+)/$",
        view=allauth_views.confirm_email,
        name="account_confirm_email"
    ),
    url(
        regex=r"^email/activation/send/$",
        view=views.account_email_verification_sent,
        name="account_email_verification_sent"
    ),
    url(
        regex=r"^email/activation/done/$",
        view=views.email_activation_done,
        name="email_activation_done"
    ),
    url(
        regex=r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        view=views.CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    url(
        regex=r'^reset/done/$',
        view=views.CustomPasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    url(
        regex=r'^social/connections/$',
        view=allauth_social_views.connections,
        name='socialaccount_connections'
    )
]
