from django.shortcuts import render
from django.http import HttpResponse
from . import sktest
from . import YelpFusion
from . import usersCustom

from django.db.models import Q

posts =  sktest.getDB()

active_user = usersCustom.userC([''])

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

def browse(request):
	return render(request, 'dumpApp/browse.html', {'title': 'Browse'})

def deals(request):
	return render(request, 'dumpApp/deals.html', {'title': 'Deals'})

def order(request):
	return render(request, 'dumpApp/order.html', {'title': 'Order'})

def search(request):
	if request.method == "POST":
		name = request.POST['myvalue']
		print(name)
	return render(request, 'dumpApp/search.html', {'title': 'Search'})

def search_results(request):
	context = {
		'name': "Narek Zamanyan"
	}

	if request.method == "POST":
		#sktest.
		name = request.POST['myvalue']
		#context['name'] = name
		#print(name)
	#list = (YelpFusion.search_yelp(request.POST['myvalue'])).split(" ")
	list = (request.POST['myvalue']).split(' ')
	context['search_results'] = YelpFusion.search_yelp('term = ' + list[0], 'location = ' + list[1])

	return render(request, 'dumpApp/search_results.html', context)


#ADDED (Master Code Online)
# def search(request):
# 	template = 'dumpApp/home.html'
#
# 	query = request.GET.get('g') #q = query variable
#
# 	#where is the table?
# 	#Q encapsulates the query
# 	#results = Post.objects.filter(Q(title__icontains=query) | Q(body__contains=query))
#
# 	#list is returned
# 	#num=1 -- object per page
# 	pages = pagination(request, results, num=1)
#
# 	context = {
# 		'items': pages[0],
# 		'page_range': pages[1],
# 	}
# 	return render(request, template, context)
#ADDED (Master Code Online)

#ADDED (Mitch)
def get_query_results(query=None):
#def search(request)
	queryset = []
	#creating a list out of all the query phrases
	#so queries is a list
	queries = query.split("")
	for q in queries:
		#???????????????????????????????????????
		#where does BlogPost come from?
		#???????????????????????????????????????
		posts = BlogPost.objects.filter(
				Q(title__icontains=q) |
				Q(body__icontains=q)
			).distinct()
		for post in posts:
			queryset.append(post)

	return list(set(queryset))
#ADDED (Mitch)

def contact(request):
	#the dictionary context is the database query

	return render(request, 'dumpApp/base.html', {})




def login(request):
	context = {}
	return render(request, 'dumpApp/login.html', context)


def register(request):
	context = {}
	return render(request, 'dumpApp/register.html', context)

def logout(request):
	context = {}
	active_user.logout()
	return render(request, 'dumpApp/logout.html', context)

def login_error(request):
	context = {}
	return render(request, 'dumpApp/login_error.html', context)

def profile(request):
	context = {}
	if request.method == "POST":
		#sktest.
		username = request.POST['username']
		password = request.POST['password']
	try:
		active_user = usersCustom.authenticate_user(username, password)
		context['email'] = active_user.email
		context['phone'] = active_user.cell
		print(active_user.is_authenticated)
		context['user_authenticated'] = active_user.is_authenticated
		return render(request, 'dumpApp/profile.html', context)
	except:
		context['error'] = "Invalid username or password. Please Try Again"
		print(active_user.is_authenticated)
		context['user_authenticated'] = active_user.is_authenticated
		return render(request, 'dumpApp/login.html', context)
