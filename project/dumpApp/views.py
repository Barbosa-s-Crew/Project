from django.shortcuts import render
from django.http import HttpResponse
from . import sktest
from . import YelpFusion
from . import usersCustom

from django.db.models import Q

posts =  sktest.getDB()

#request.session['active_user'] = usersCustom.userC([''])
def check_user(request):
	try:
		if not request.session['is_authenticated']:
			request.session['is_authenticated'] = False
		else:
			request.session['is_authenticated'] = True
	except:
		request.session['is_authenticated'] = False

def home(request):
	check_user(request)
	context = {
		'deals': deals,
		'user_authenticated': request.session['is_authenticated']
	}
	return render(request, 'dumpApp/home.html', context)

def dump(request):
	check_user(request)
	context = {
		'table': posts
	}
	return render(request, 'dumpApp/dump.html', context)
	
def about(request):
	check_user(request)
	context = {
		'title': 'About',
		'user_authenticated': request.session['is_authenticated']
	}
	return render(request, 'dumpApp/about.html', context)

def browse(request):
	check_user(request)
	context = {
		'title': 'Browse',
		'user_authenticated': request.session['is_authenticated']
	}
	return render(request, 'dumpApp/browse.html', context)

def deals(request):
	check_user(request)
	context = {
		'title': 'Deals',
		'user_authenticated': request.session['is_authenticated']
	}
	return render(request, 'dumpApp/deals.html', context)

def order(request):
	check_user(request)
	context = {
		'title': 'Order',
		'user_authenticated': request.session['is_authenticated']
	}
	return render(request, 'dumpApp/order.html', context)

def search(request):
	check_user(request)
	context = {
		'table': posts,
		'title': 'Search',
		'user_authenticated': request.session['is_authenticated']
	}
	if request.method == "POST":
		name = request.POST['myvalue']
		print(name)
	return render(request, 'dumpApp/search.html', context)

def search_results(request):
	check_user(request)
	context = {
		'name': "Narek Zamanyan",
		'user_authenticated': request.session['is_authenticated']
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
	check_user(request)
	#the dictionary context is the database query

	return render(request, 'dumpApp/base.html', {})

def login(request):
	check_user(request)
	context = {}
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
	else:
		return render(request, 'dumpApp/login.html', context)

	try:
		user = usersCustom.authenticate_user(username, password)
		request.session['email'] = user.email
		request.session['cell'] = user.cell
		request.session['is_authenticated'] = user.is_authenticated
		print(request.session['is_authenticated'])
		context['user_authenticated'] = request.session['is_authenticated']
		return render(request, 'dumpApp/profile.html', context)
	except:
		print("Error is true")
		context['error'] = "Invalid username or password"
		return render(request, 'dumpApp/login.html', context)

def register(request):
	check_user(request)
	context = {}

	if request.method == "POST":
		email = request.POST['email']
		password = request.POST['password']
	else:
		return render(request, 'dumpApp/register.html', context)
	try:
		user_created = usersCustom.create_user(email, password)
		if(user_created == True):
			return render(request, 'dumpApp/login.html', context)
		else:
			context['error'] = "User Already Exist with that email"
			return render(request, 'dumpApp/register.html', context)
	except:
		context['error_1'] = "Database failure"
		return render(request, 'dumpApp/register.html', context)


def logout(request):
	check_user(request)
	context = {}
	request.session.flush()
	return render(request, 'dumpApp/logout.html', context)

def login_error(request):
	check_user(request)
	context = {}
	return render(request, 'dumpApp/login_error.html', context)

def profile(request):
	check_user(request)
	context = {
		'user_authenticated': request.session['is_authenticated'],
		'email': request.session['email'],
		'phone': request.session['cell']
	}
	try:
		if request.session['is_authenticated']:
			return render(request, 'dumpApp/profile.html', context)
		else:
			return login(request)
	except:
		return login(request)

def restaurants(request):
	check_user(request)

	#the dictionary context is the database query
	context = {}
	# 	'name': "Narek Zamanyan",
	# 	'user_authenticated': request.session['is_authenticated']
	# }

	if request.method == "POST":
	# 	#sktest.
		restaurant = YelpFusion.search_restaurant(request.POST['id'])
		context['everything'] = restaurant
		schedule = {}
		#context['formatted_schedule']
		#for i in range(5):
		#if i == 0:
		schedule['Monday'] = restaurant['hours'][0]['open'][0]['start'][:2] + ":" + restaurant['hours'][0]['open'][0]['start'][2:]
		schedule['Monday'] = schedule['Monday'] + ' - '
		schedule['Monday'] = schedule['Monday'] + restaurant['hours'][0]['open'][0]['end'][:2] + ":" + restaurant['hours'][0]['open'][0]['end'][2:] 
		schedule['Monday'] = 'Monday   ' + schedule['Monday']

		schedule['Tuesday'] = restaurant['hours'][0]['open'][0]['start'][:2] + ":" + restaurant['hours'][0]['open'][0]['start'][2:]
		schedule['Tuesday'] = schedule['Tuesday'] + ' - '
		schedule['Tuesday'] = schedule['Tuesday'] + restaurant['hours'][0]['open'][0]['end'][:2] + ":" + restaurant['hours'][0]['open'][0]['end'][2:] 
		schedule['Tuesday'] = 'Tuesday   ' + schedule['Tuesday']

		schedule['Wednesday'] = restaurant['hours'][0]['open'][0]['start'][:2] + ":" + restaurant['hours'][0]['open'][0]['start'][2:]
		schedule['Wednesday'] = schedule['Wednesday'] + ' - '
		schedule['Wednesday'] = schedule['Wednesday'] + restaurant['hours'][0]['open'][0]['end'][:2] + ":" + restaurant['hours'][0]['open'][0]['end'][2:] 
		schedule['Wednesday'] = 'Wednesday   ' + schedule['Wednesday']

		schedule['Thursday'] = restaurant['hours'][0]['open'][0]['start'][:2] + ":" + restaurant['hours'][0]['open'][0]['start'][2:]
		schedule['Thursday'] = schedule['Thursday'] + ' - '
		schedule['Thursday'] = schedule['Thursday'] + restaurant['hours'][0]['open'][0]['end'][:2] + ":" + restaurant['hours'][0]['open'][0]['end'][2:] 
		schedule['Thursday'] = 'Thursday   ' + schedule['Thursday']

		schedule['Friday'] = restaurant['hours'][0]['open'][0]['start'][:2] + ":" + restaurant['hours'][0]['open'][0]['start'][2:]
		schedule['Friday'] = schedule['Friday'] + ' - '
		schedule['Friday'] = schedule['Friday'] + restaurant['hours'][0]['open'][0]['end'][:2] + ":" + restaurant['hours'][0]['open'][0]['end'][2:] 
		schedule['Friday'] = 'Friday   ' + schedule['Friday']

		print(restaurant['hours'])
		#schedule['Monday'] += "-"
		#schedule['Monday'] += restaurant.hours
		context['schedule'] = schedule
	 	# context['photos'] = restaurant.photos
	 	# context['image_url'] = request.POST['image_url']
	 	# context['phone'] = request.POST['phone']
	 	# photos_array = request.POST['photos']
	 	# context['array'] = photos_array
	 	# context['location'] = request.POST['location']
	 	# context['hours'] = request.POST['hours']
	 	# context['is_closed'] = request.POST['is_closed']
	 	# print(request.POST['photos'])
	# 	#context['name'] = name
	# 	#print(name)
	# #list = (YelpFusion.search_yelp(request.POST['myvalue'])).split(" ")
	# list = (request.POST['myvalue']).split(' ')
	# context['search_results'] = YelpFusion.search_yelp('term = ' + list[0], 'location = ' + list[1])


	return render(request, 'dumpApp/restaurants.html', context)

