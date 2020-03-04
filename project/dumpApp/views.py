from django.shortcuts import render
from django.http import HttpResponse
from . import sktest

posts =  sktest.getDB()

def home(request):
	return render(request, 'dumpApp/home.html')

def dump(request):
	context = {
		'table': posts
	}
	return render(request, 'dumpApp/dump.html', context)

def about(request):
	return render(request, 'dumpApp/about.html')


