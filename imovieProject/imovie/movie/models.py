from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField

# Create your models here.
<<<<<<< HEAD
class Category(models.Model):

	name = models.CharField(max_length=200,
							db_index=True)
	slug = models.SlugField(max_length=200,
							db_index=True,
							unique=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('movies:movie_list_by_category',
						args=[self.slug])

class Movie(models.Model):

	category = models.ForeignKey(Category,
								related_name='movies')
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200,blank=True)
	director = models.CharField(max_length=200)
	scriptwriter = models.CharField(max_length=200)
	nation = models.CharField(max_length=100)
	star = models.CharField(max_length=200)
	length = models.CharField(max_length=100)

	year = models.DecimalField(max_digits=19,decimal_places=0)
	language = models.CharField(max_length=200,blank=True, null=True)

	description = models.TextField(blank=True)
	poster = models.ImageField(upload_to='movies/%Y/%m/%d',blank=True)
	rank = models.DecimalField(max_digits=10, decimal_places=2)



	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	users_like = models.ManyToManyField(User,
									related_name='movies_liked',
									blank=True) 
	video = EmbedVideoField(default="")

	class Meta:
		ordering = ('name',)
		index_together = (('id', 'slug'),)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('movies:movie_detail',
						args=[self.id,self.slug])

	def get_comment_url(self):
		return reverse('movies:movie_comment',
						args=[self.id,self.slug])


=======
class Activity(models.Model):

	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200)
	body = models.TextField()
	active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	date = models.DateField(blank=True, null=True)
	todate = models.DateField(blank=True,null=True)

	class Meta:
		ordering = ('created',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('movies:activity_detail',
						args=[self.id,self.slug])
>>>>>>> zheliu
