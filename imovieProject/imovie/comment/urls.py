from django.conf.urls import url
from . import views

urlpatterns = [

	url(r'^movie-detail/(?P<id>\d+)/$', views.comment_detail, 
		name='comment_detail'),
	url(r'^review-list/$', views.comment_list, name='comment_list'),
]