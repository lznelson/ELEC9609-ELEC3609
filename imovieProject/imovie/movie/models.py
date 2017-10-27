from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField

# Create your models here.
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
