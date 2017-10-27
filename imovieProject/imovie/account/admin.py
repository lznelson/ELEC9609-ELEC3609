from django.contrib import admin
from .models import Profile



class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth','id']
    list_filter = ['user']

admin.site.register(Profile, ProfileAdmin)
