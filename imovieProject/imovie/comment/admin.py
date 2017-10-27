from django.contrib import admin
from .models import ShortComment, Comment, AnotherComment
# Register your models here.


class ShortCommentAdmin(admin.ModelAdmin):
	list_display = ['author', 'movie','created']
	list_filter = ['movie']

admin.site.register(ShortComment, ShortCommentAdmin)

class CommentAdmin(admin.ModelAdmin):
	list_display = ['author', 'movie','created']
	list_filter = ['movie','created']
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(Comment, CommentAdmin)

class AnotherCommentAdmin(admin.ModelAdmin):
	list_display=['author','created','comment']

admin.site.register(AnotherComment, AnotherCommentAdmin)



