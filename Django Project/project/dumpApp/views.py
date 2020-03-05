from django.shortcuts import render
from django.http import HttpResponse
from . import sktest

posts =  sktest.getDB()

deals = [
	{
		'name': 'Deal 1',
		'food_type': 'Deal Type 1',
		'restaurant': 'Restaurant 1',
		'price': '$11',
		'rating': '4.5 Stars',
		'is_saved': 'false',
		'duration': '20-30 min',
		'items': 'item_1'
	},
	{
		'name': 'Deal 2',
		'food_type': 'Deal Type 2',
		'restaurant': 'Restaurant 2',
		'price': '$22',
		'rating': '3 Stars',
		'ss_saved': 'true',
		'duration': '30-35 min',
		'items': 'item_2'
		}
]

def home(request):
	context_deals = {
		'deals': deals
	}
	return render(request, 'dumpApp/home.html', context_deals)

def dump(request):
	context = {
		'table': posts
	}
	return render(request, 'dumpApp/dump.html', context)

def about(request):
	return render(request, 'dumpApp/about.html', {'title': 'About'})
