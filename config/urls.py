from django.conf.urls import include, url
from django.contrib import admin

from allauth.socialaccount import views as allauth_social_views

urlpatterns = [
    url(
        r'^admin/',
        include('admin_honeypot.urls', namespace='admin_honeypot')
    ),
    # TODO: Change the actual url to your admin.
    url(
        r'^asecreturlforyouradmin/',
        admin.site.urls
    ),
    url(
        r'^api/',
        include('config.api_urls', namespace="api")
    ),
    url(
        r'^auth/',
        include('accounts.urls', namespace="accounts")
    ),
    # Set up signup route here, since we can't hook into allauth's
    # _process_signup method. There reverse gets called harcoded with
    # ('socialaccount_signup'). See allauth/socialaccount/helpers.py
    # in line 24.
    url(
        r'^auth/social/signup/$',
        allauth_social_views.signup,
        name='socialaccount_signup'
    ),
]
