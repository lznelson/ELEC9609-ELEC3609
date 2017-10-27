from django.conf.urls import url
from . import views

urlpatterns = [

	url(r'^movie-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.movie_detail, 
		name='movie_detail'),
	url(r'^movie-list/$', views.movie_list, name='movie_list'),

	url(r'^activity-list/$', views.activity_list, name='activity_list'),
	url(r'^activity-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.activity_detail, 
		name='activity_detail'),

]
