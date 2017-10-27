from django.shortcuts import render, get_object_or_404
from .models import Movie, Category, Activity
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from account.models import User
from comment.forms import ShortCommentForm, CommentForm
from django.http import HttpResponse, JsonResponse
from comment.models import ShortComment
from django.db.models import Avg, Sum

from .forms import SearchForm
from haystack.query import SearchQuerySet
from ajaxDecorators.decorators import ajax_required
import redis
from django.conf import settings

from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect

#from django.utils.safestring import mark_safe
#import markdown
# Create your views here.


@login_required
@cache_page(60*15)
@csrf_protect
def movie_comment(request,id,slug):
	movie = get_object_or_404(Movie,
						id=id,
						slug=slug)
	
	author = request.user
	new_comment =None
	if request.method=="POST":
		comment_form = CommentForm(data=request.POST)	
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.movie = movie
			new_comment.author = author 
			new_comment.save()
	else:
		comment_form = CommentForm()

	return render(request,
				'movies/movie/review.html',
				{'author':author,
				'movie':movie,
				'new_comment':new_comment,
				'comment_form':comment_form})
	
@login_required
@require_POST
@ajax_required
def movie_like(request):
	movie_id = request.POST.get('id')
	action =request.POST.get('action')
	if movie_id and action:
		try:
			movie = Movie.objects.get(id=movie_id)
			if action == 'like':
				movie.users_like.add(request.user)
			else:
				movie.users_like.remove(request.user)
			return JsonResponse({'status':'ok'})
		except:
			pass
	return JsonResponse({'status':'ko'})


def movie_ranking(request):
	
	movie_ranking = r.zrange('movie_ranking',0,-1,desc=True)[:6]
	movie_ranking_ids = [int(id) for id in movie_ranking]
	movie_viewed = list(Movie.objects.filter(id__in=movie_ranking_ids))
	movie_viewed.sort(key=lambda x: movie_ranking_ids.index(x.id))
	movies = movie_viewed

	movies_by_rank = Movie.objects.order_by('-rank')[:6]

	return render(request,
				"movies/movie/movie_ranking.html",
				{"movie_viewed":movie_viewed,
				"movies":movies,
				"movies_by_rank":movies_by_rank})

	@cache_page(60*15)
@csrf_protect
def movie_list(request, category_slug=None):
	category = None
	categories = Category.objects.all()
	movies = Movie.objects.all()
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		movies = movies.filter(category=category)
	else:
		movies = Movie.objects.all()

	paginator = Paginator(movies, 8)
	page = request.GET.get('page')
	try:
		movies = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer deliver the first page
		movies = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			# If the request is AJAX and the page is out of range return an empty page
			return HttpResponse('')
			# If page is out of range deliver last page of results
			movies = paginator.page(paginator.num_pages)
		if request.is_ajax():
			return render(request,
					'movies/movie/list_ajax.html',
					{'section': 'movies', 
					'movies': movies})

	form = SearchForm()
	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			cd = form.cleaned_data
			results = SearchQuerySet().models(Movie).filter(content=cd['query']).load_all()
			# count total results
			total_results = results.count()
		return render(request, 'movies/movie/list.html',
								{'form': form,
								'cd': cd,
								'results': results,
								'total_results': total_results})

	return render(request,
				'movies/movie/list.html',
				{'section': 'movies',
				'movies': movies,
				'form': form,
				'category':category,
				'categories':categories})
	@cache_page(60*15)
@csrf_protect
def movie_detail(request, id, slug):
	movie = get_object_or_404(Movie,
							id=id,
							slug=slug)

	total_views = r.incr('movie:{}:views'.format(movie.id))
	r.zincrby('movie_ranking',movie.id,1)

	#add shortcomment 
	author = request.user
	shortcomments = movie.shortcomments.filter(active=True)
	comments = movie.comments.filter(active=True)

	new_shortcomment =None
	if request.method=="POST":
		shortcomment_form = ShortCommentForm(data=request.POST)	
		if shortcomment_form.is_valid():
			new_shortcomment = shortcomment_form.save(commit=False)
			new_shortcomment.movie = movie
			new_shortcomment.author = author 
			new_shortcomment.save()
	else:
		shortcomment_form = ShortCommentForm()

	#rank
	if shortcomments.exists():
		rank = ShortComment.objects.filter(movie_id=id).aggregate(avg_ranking=Avg('rank'))
		movie.rank = rank['avg_ranking']			
	else:
		rank = movie.rank
	movie.save()

	return render(request,
					'movies/movie/detail.html',
					{'movie':movie,
					'author':author,
					'section': 'movies',
					'shortcomments':shortcomments,
					'comments':comments,
					'new_shortcomment':new_shortcomment,
					'shortcomment_form':shortcomment_form,
					'total_views':total_views})

def activity_list(request):
	activities = Activity.objects.all()

	return render(request,
				"activity/activity_list.html",
				{"activities":activities})


def activity_detail(request,id,slug):
	activity = get_object_or_404(Activity,
							        	id=id,
							        	slug=slug)

	return render(request,
				"activity/activity_detail.html",
				{"activity":activity})



