from django.contrib import admin
from .models import Category, Movie, Activity

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)


class MovieAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug','rank','nation','length']
	list_filter = ['rank', 'created', 'updated','nation']
	search_fields = ('name', 'year')
	#list_editable = ['rank', 'name', 'nation']
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Movie, MovieAdmin)

