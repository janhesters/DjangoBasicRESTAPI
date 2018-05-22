from django.conf.urls import url
from rest_auth import views as rest_auth_views
from rest_auth.registration import views as rest_auth_registration_views

from . import views

urlpatterns = [
    # URLs that do not require a session or valid token
    url(
        regex=r'^login/$',
        view=rest_auth_views.LoginView.as_view(),
        name='login'
    ),
    url(
        regex=r'^password/reset/$',
        view=rest_auth_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    url(
        regex=r'^registration/$',
        view=rest_auth_registration_views.RegisterView.as_view(),
        name='register'
    ),
    url(
        regex=r'^facebook/$',
        view=views.FacebookLogin.as_view(),
        name='fb_login'
    ),
    url(
        regex=r'^facebook/connect/$',
        view=views.FacebookConnect.as_view(),
        name='fb_connect'
    ),
    # URLs that require a user to be logged in with a valid session / token.
    url(
        regex=r'^logout/$',
        view=rest_auth_views.LogoutView.as_view(),
        name='logout'
    ),
    url(
        regex=r'^user/$',
        view=rest_auth_views.UserDetailsView.as_view(),
        name='user_details'
    ),
    url(
        regex=r'^password/change/$',
        view=rest_auth_views.PasswordChangeView.as_view(),
        name='password_change'
    ),
]
