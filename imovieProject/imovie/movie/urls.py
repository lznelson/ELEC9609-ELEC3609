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

