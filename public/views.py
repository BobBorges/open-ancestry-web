from django.shortcuts import render
from ancestry_web.instance_details import this_instance
# Create your views here.

def landing_page(request):
	context = {}
	context.update(this_instance)
	return render(request, 'public/landing-page.html', context)

def statistics(request):
	context= {}
	return render(request, 'public/stats.html', context)

def about(request):
	context = {}
	return render(request, 'public/about.html', context)