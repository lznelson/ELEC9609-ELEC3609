from django.shortcuts import render

# Create your views here.
def home(request):
	context = locals()
	template = 'home.html'
	return render(request,template,context)

def about(request):
	context = locals()
	template = 'about.html'
	return render(request,template,context)

def personal(request):
	context = locals()
	template = 'personal.html'
	return render(request,template,context)

def activities(request):
	context = locals()
	template = 'activities.html'
	return render(request,template,context)

def detail(request):
	context = locals()
	template = 'detail.html'
	return render(request,template,context)