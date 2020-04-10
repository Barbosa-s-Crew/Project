from django.shortcuts import render
from django.http import HttpResponse
from . import sktest
from . import YelpFusion
from . import usersCustom
from . import deals as dealsmodule
from . import restaurant as restaurant_module

from django.db.models import Q

posts =  sktest.getDB()
#--------------------------------------Helper Functions -----------------------------

#request.session['active_user'] = usersCustom.userC([''])
def check_user(request):
	try:
		if not request.session['is_authenticated']:
			request.session['is_authenticated'] = False
		else:
			request.session['is_authenticated'] = True
	except:
		request.session['is_authenticated'] = False

#-------------------------------------- Views ------------------------------------

def home(request):
	check_user(request)
	context = {
		'user_authenticated': request.session['is_authenticated'],
		'deals': dealsmodule.get_deals()
	}
	if context['user_authenticated'] == False:
		return render(request, 'dumpApp/home.html', context)

	context['recommendations'] = restaurant_module.get_favorites_using_user_ID(request.session['ID'])
	context['recent_orders'] = restaurant_module.get_recent_using_user_ID(request.session['ID'])

	# If logged in, go to dashboard instead
	return render(request, 'dumpApp/dashboard.html', context)

def dashboard(request):
	check_user(request)
	context = {
		'deals': dealsmodule.get_deals(),
		'recommendations': restaurant_module.get_favorites_using_user_ID(),
		'recent_orders': restaurant_module.get_recent_using_user_ID(request.session['ID']),
		'user_authenticated': request.session['is_authenticated']
	}
	print("DEBUG" + str(context['recommendations']))
	if content['user_authenticated'] == True:
		return render(request, 'dumpApp/dashboard.html', context)
	# If not logged in, go to home page instead
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
	context['search_results_db'] = restaurant_module.get_restaurant_using_keyword(list[0])
	print(context['search_results_db'])
	context['search_results'] = YelpFusion.search_yelp('term = ' + list[0], 'location = ' + list[1])

	return render(request, 'dumpApp/search_results.html', context)

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
		request.session['ID'] = user.ID
		request.session['username'] = user.username
		request.session['email'] = user.email
		request.session['cell'] = user.cell
		request.session['payment_option'] = user.payment_option
		request.session['photo'] = user.photoURL
		#request.session['gender'] = user.gender
		request.session['preferences'] = user.other_info
		request.session['is_authenticated'] = user.is_authenticated

		print(user.username)


		print(request.session['is_authenticated'])
		context['user_authenticated'] = request.session['is_authenticated']
		context['recommendations'] = restaurant_module.get_favorites_using_user_ID()
		context['recent_orders'] = restaurant_module.get_recent_using_user_ID(request.session['ID'])
		context['deals'] = dealsmodule.get_deals()
		return render(request, 'dumpApp/dashboard.html', context)
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
		username = request.POST['username']
		phone = request.POST['phone']
	else:
		return render(request, 'dumpApp/register.html', context)
	try:
		user_created = usersCustom.create_user(email, password, username, phone)
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
		'phone': request.session['cell'],
		'username': request.session['username'],
		'payment_option': request.session['payment_option'],
		'photo': request.session['photo'],
		'preferences': request.session['preferences']
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

		print(request.POST['Yelp'])
		if request.POST['Yelp'] == "True":
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

			context['schedule'] = schedule
		else:
			print(request.POST['id'])

			restaurant = restaurant_module.get_restaurant_using_ID(request.POST['id'])
			context['restaurants'] = restaurant[0] 

			items = restaurant_module.get_menu_items_using_restaurant_ID(request.POST['id'])
			context['rest_items'] = items
			

			#ID=rest[0], Name=rest[1], Location_ID=rest[2], Category=rest[3], Cuisine=rest[4], Notes=rest[5], Image=rest[6])

	return render(request, 'dumpApp/restaurants.html', context)
