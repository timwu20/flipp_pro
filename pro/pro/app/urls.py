from django.conf.urls import url
from . import views
import django_cas_ng
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^login$', django_cas_ng.views.login, name='cas_ng_login'),
    url(r'^accounts/logout$', django_cas_ng.views.logout, name='cas_ng_logout'),
    url(r'^accounts/callback$', django_cas_ng.views.callback, name='cas_ng_proxy_callback'),
]
