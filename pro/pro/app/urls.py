from django.conf.urls import url
from . import views
import django_cas_ng

app_name = 'app'
urlpatterns = [
    url(r'^$', views.index, name='index'),

	## Edit team ##
	# url(r'^(?P<u_id>[0-9]+)/add/$', views.addTeam, name='add'),
	#Order matters here for reason look into url for django
	url(r'^(?P<uid>[0-9]+)/(?P<option>.*)/edited/$', views.editTeam, name='edit'),
	url(r'^(?P<uid>[0-9]+)/(?P<option>.*)/$', views.showEmployees, name='show'),

	## SSO ##
    url(r'^accounts/login$', django_cas_ng.views.login, name='cas_ng_login'),
    url(r'^accounts/logout$', django_cas_ng.views.logout, name='cas_ng_logout'),
    url(r'^accounts/callback$', django_cas_ng.views.callback, name='cas_ng_proxy_callback'),
]
