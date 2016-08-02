from django.conf.urls import url
from . import views
import django_cas_ng

app_name = 'app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^(?P<coach_id>[0-9]+)/add/$', views.addTeam, name='add'),

	## SSO ##
    url(r'^accounts/login$', django_cas_ng.views.login, name='cas_ng_login'),
    url(r'^accounts/logout$', django_cas_ng.views.logout, name='cas_ng_logout'),
    url(r'^accounts/callback$', django_cas_ng.views.callback, name='cas_ng_proxy_callback'),
]
