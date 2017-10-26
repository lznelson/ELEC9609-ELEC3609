from django.shortcuts import render, get_object_or_404
from .models import Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ajaxDecorators.decorators import ajax_required
from django.http import HttpResponse
from .forms import AnotherCommentForm
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect


@cache_page(60*15)
@csrf_protect
def comment_detail(request,id):
	comment = get_object_or_404(Comment, id=id)

	author = request.user
	anothercomments = comment.anothercomments.filter(active=True)

	new_anothercomment =None
	if request.method=="POST":
		anothercomment_form = AnotherCommentForm(data=request.POST)	
		if anothercomment_form.is_valid():
			new_anothercomment = anothercomment_form.save(commit=False)
			new_anothercomment.comment = comment
			new_anothercomment.author = author 
			new_anothercomment.save()
	else:
		anothercomment_form = AnotherCommentForm()

	return render(request,
				'comments/comment/comment_detail.html',
				{'comment':comment,
				'anothercomment_form':anothercomment_form,
				'new_anothercomment':new_anothercomment,
				'anothercomments':anothercomments})


def comment_list(request):
	comments = Comment.objects.all()

	paginator = Paginator(comments, 6)
	page = request.GET.get('page')
	try:
		comments = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer deliver the first page
		comments = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			# If the request is AJAX and the page is out of range return an empty page
			return HttpResponse('')
			# If page is out of range deliver last page of results
			comments = paginator.page(paginator.num_pages)
		if request.is_ajax():
			return render(request,
					'comments/comment/list_ajax.html',
					{'comments': comments})

	return render(request,
			'comments/comment/comment_list.html',
			{'comments': comments,
			'page': page})
