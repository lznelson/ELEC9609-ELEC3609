from django.db import models
from django.utils import timezone
from movie.models import Movie
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse



# Create your models here.
class ShortComment(models.Model):
	author = models.ForeignKey(User,
							related_name='shortcomments')
	movie = models.ForeignKey(Movie,
							related_name='shortcomments')
	body = models.TextField(max_length=400)
	created = models.DateTimeField(auto_now_add=True)
	rank = models.DecimalField(max_digits=10, decimal_places=2)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return 'Shortcomment by {} in {}'.format(self.author,self.created)

	def get_author_url(self):
		author = self.author
		return author

	def get_movie_url(self):
		movie = self.movie
		return movie


class Comment(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200)

	author = models.ForeignKey(User,
							related_name='comments')
	movie = models.ForeignKey(Movie,
							related_name='comments')
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	#rank = models.DecimalField(max_digits=10, decimal_places=2)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('-created',)

	def get_author_url(self):
		author = self.author
		return author

	def get_movie_url(self):
		movie = self.movie
		return movie

	def get_absolute_url(self):
		return reverse('comments:comment_detail',
					args=[self.id])

class AnotherComment(models.Model):
	body = models.TextField(max_length=400)
	author = models.ForeignKey(User,
							related_name='anothercomments')
	comment = models.ForeignKey(Comment,
							related_name='anothercomments',default="")
	created = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	def get_author_url(self):
		author = self.author
		return author

