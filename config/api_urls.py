from django.conf.urls import include, url

urlpatterns = [
    url(r'^auth/', include('accounts.api.urls', namespace="auth")),
]
