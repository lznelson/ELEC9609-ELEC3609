from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	date_of_birth = models.DateField(blank=True, null=True)
	photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
	
	def __str__(self):
		return 'Profile for user {}'.format(self.user.username)

	def get_absolute_url(self):
		user = self.user
		return reverse('user_detail',
				args=[user.username])



