from django.conf.urls import url
from . import views

urlpatterns = [
	
	url(r'^like/$', views.movie_like, name='movie_like'),	
	url(r'^movie-comment/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.movie_comment, 
		name='movie_comment'),
	url(r'^movie-ranking/$', views.movie_ranking, name='movie_ranking'),
	url(r'^(?P<category_slug>[-\w]+)/$', views.movie_list, 
		name='movie_list_by_category'),

]

urlpatterns = [
 
 	url(r'^movie-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.movie_detail, 
 		name='movie_detail'),
 	url(r'^movie-list/$', views.movie_list, name='movie_list'),
 
 	url(r'^activity-list/$', views.activity_list, name='activity_list'),
 	url(r'^activity-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.activity_detail, 
 		name='activity_detail'),
 
 ]