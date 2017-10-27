from django import forms
from django.contrib.auth.models import User
from .models import ShortComment, Comment, AnotherComment

class ShortCommentForm(forms.ModelForm):
	class Meta:
		model = ShortComment
		fields = ('rank','body')

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('title','body')

class AnotherCommentForm(forms.ModelForm):
	class Meta:
		model = AnotherComment
		fields = ('body',)
