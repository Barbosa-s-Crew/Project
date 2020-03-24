from django.shortcuts import render
from django.http import HttpResponse
from . import sktest
from . import YelpFusion
from . import usersCustom

from django.db.models import Q

posts =  sktest.getDB()

active_user = usersCustom.userC([''])

def home(request):
	global active_user
	context = {
		'deals': deals,
		'user_authenticated': active_user.is_authenticated
	}
	try:
		print(active_user['username'])
	except:
		print("Not there")
	return render(request, 'dumpApp/home.html', context)

def dump(request):
	global active_user
	context = {
		'table': posts
	}
	return render(request, 'dumpApp/dump.html', context)

def about(request):
	global active_user
	context = {
		'title': 'About',
		'user_authenticated': active_user.is_authenticated
	}
	return render(request, 'dumpApp/about.html', context)

def browse(request):
	global active_user
	context = {
		'title': 'Browse',
		'user_authenticated': active_user.is_authenticated
	}
	return render(request, 'dumpApp/browse.html', context)

def deals(request):
	global active_user
	context = {
		'title': 'Deals',
		'user_authenticated': active_user.is_authenticated
	}
	return render(request, 'dumpApp/deals.html', context)

def order(request):
	global active_user
	context = {
		'title': 'Order',
		'user_authenticated': active_user.is_authenticated
	}
	return render(request, 'dumpApp/order.html', context)

def search(request):
	global active_user
	context = {
		'table': posts,
		'user_authenticated': active_user.is_authenticated
	}
	if request.method == "POST":
		name = request.POST['myvalue']
		print(name)
	return render(request, 'dumpApp/search.html', {'title': 'Search'})

def search_results(request):
	global active_user
	context = {
		'name': "Narek Zamanyan",
		'user_authenticated': active_user.is_authenticated
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
	global active_user
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
	global active_user
	context = {}
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
	else:
		return render(request, 'dumpApp/login.html', context)

	try:
		active_user = usersCustom.authenticate_user(username, password)
		context['email'] = active_user.email
		context['phone'] = active_user.cell
		print(active_user.is_authenticated)
		context['user_authenticated'] = active_user.is_authenticated
		return render(request, 'dumpApp/profile.html', context)
	except:
		print("Error is true")
		context['error'] = "Invalid username or password"
		return render(request, 'dumpApp/login.html', context)

def register(request):
	global active_user
	context = {}
	return render(request, 'dumpApp/register.html', context)

def logout(request):
	global active_user
	context = {}
	active_user.logout()
	return render(request, 'dumpApp/logout.html', context)

def login_error(request):
	global active_user
	context = {}
	return render(request, 'dumpApp/login_error.html', context)

def profile(request):
	global active_user
	context = {
		'user_authenticated': active_user.is_authenticated
	}
	if active_user['is_authenticated']:
		return render(request, 'dumpApp/profile.html', context)
	else:
		login(request)
