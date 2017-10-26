from django.conf.urls import url
from . import views

from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import password_change
from django.contrib.auth.views import password_change_done
from django.contrib.auth.views import password_reset
from django.contrib.auth.views import password_reset_done
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth.views import password_reset_complete


urlpatterns = [
		
	#login logout
	url(r'^login/$', views.login_and_register, name='login'),
	url(r'^logout/$', logout, name='logout'),
	url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),
	
	#change password
	url(r'^password-change/$', password_change, 
		{'template_name': 'registration/password_form.html'}, 
		name='password_change'),
	url(r'^password-change/done/$', password_change_done, 
		{'template_name': 'registration/password_change_done.html'},
		name='password_change_done'),
	
	#reset password
	#restore password urls
	url(r'^password-reset/$',password_reset,
		name='password_reset'),
	url(r'^password-reset/done/$',password_reset_done,
		name='password_reset_done'),
	url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
		password_reset_confirm,
		name='password_reset_confirm'),
	url(r'^password-reset/complete/$',
		password_reset_complete,
	name='password_reset_complete'),

	#view your dashborad
	url(r'^dashboard/$', views.dashboard, name='dashboard'),

	#edit profile
	url(r'^edit/$', views.edit, name='edit'),

	url(r'^user-detail/(?P<username>[-\w]+)/$', views.user_detail, name='user_detail'),

	#url(r'^users/(?P<username>[-\w]+)/$',
		#views.user_detail,
		#name='user_detail'),

	#url(r'^users/follow/$', views.user_follow, name='user_follow'),


]
