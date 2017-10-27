from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import Profile

from django.contrib import messages

from account.models import User
from movie.models import Movie
from comment.models import ShortComment, Comment

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from movie.forms import SearchForm
from haystack.query import SearchQuerySet

import redis
from django.conf import settings

from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect

#from decimal import Decimal

@cache_page(60*15)
@csrf_protect
def login_and_register(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(username=cd['username'],
								password=cd['password'])
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/account/')
			else:
				messages.error(request,'Disabled account')
		else:
			messages.error(request,'Invalid login')
			#return render(request,'registration/login.html',{'error_info': '密码错误'})
			#return HttpResponse('触发ajax')
	else:
		form = LoginForm()

	if request.method =='POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			#Create a new user object but avoid saving it yet
			new_user = user_form.save(commit=False)
			#Set the chosen password
			new_user.set_password(user_form.cleaned_data['password'])
			#Save the User object
			new_user.save()
			#Create the user profile
			profile = Profile.objects.create(user=new_user)
			#add action stream
			#create_action(new_user, 'has created an account')
			return render(request,
						'account/login_and_register.html',
						{'new_user':new_user})
	else:
		user_form = UserRegistrationForm()
	return render(request, 
				'account/login_and_register.html', 
				{'form': form,
				'user_form':user_form})


@login_required
def dashboard(request):

	author = request.user.id
	#shortcomment list
	shortcomments = ShortComment.objects.filter(author_id=author)
	comments = Comment.objects.filter(author_id=author)
	#my movie list
	movies = Movie.objects.filter(users_like=author)

	paginator = Paginator(shortcomments,8)
	page = request.GET.get('page')
	try:
		shortcomments = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer deliver the first page
		shortcomments = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			# If the request is AJAX and the page is out of range return an empty page
			return HttpResponse('')
			# If page is out of range deliver last page of results
			shortcomments = paginator.page(paginator.num_pages)
		if request.is_ajax():
			return render(request,
					'account/dashboard.html',
					{'section': 'dashboard', 
					'shortcomments': shortcomments})

	return render(request,
				'account/dashboard.html',
				{'section': 'dashboard',
				'shortcomments':shortcomments,
				'comments':comments,
				'movies':movies})


@login_required
def edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user,
								 data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile,
									   data=request.POST,
									   files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Profile updated successfully')
		else:
			messages.error(request, 'Error updating your profile')
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)
	return render(request, 'account/edit.html', {'user_form': user_form,
												 'profile_form': profile_form})

@login_required
def user_detail(request,username):
	
	user= get_object_or_404(User,username=username)
	shortcomments = ShortComment.objects.filter(author_id=user)
	comments = Comment.objects.filter(author_id=user)
	movies = Movie.objects.filter(users_like=user)
	return render(request,
				'account/user_detail.html',
				{'user':user,
				'shortcomments':shortcomments,
				'comments':comments,
				'movies':movies})

def movie_detail(request, id, slug):
	movie = get_object_or_404(Movie,
							id=id,
							slug=slug)
	r.zincrby('movie_ranking',movie.id,1)
	return 

@login_required
def home(request):
	movies = Movie.objects.all()
	shortcomments = ShortComment.objects.all()
	comments = Comment.objects.all()


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
				'account/home.html',
				{'section': 'home',
				'movies':movies,
				'shortcomments':shortcomments,
				'comments':comments})	
