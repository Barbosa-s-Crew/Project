from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from . import sktest
from . import YelpFusion
from . import usersCustom
from . import deals as dealsmodule
from . import restaurant as restaurant_module
from . import submitOrder as order_module
from . import writeReview as review_module
import ast

from django.db.models import Q

posts =  sktest.getDB()
#--------------------------------------Helper Functions -----------------------------


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
	if request.session['is_authenticated'] == False:
		return render(request, 'dumpApp/home.html', context)

	context['recommendations'] = restaurant_module.get_favorites_using_user_ID(request.session['ID'])
	context['recent_orders'] = restaurant_module.get_recent_using_user_ID(request.session['ID'])

	# If logged in, go to dashboard instead
	return redirect('dashboard')

def dashboard(request):
	check_user(request)

	if request.session['is_authenticated'] == False:
		return redirect('login')
	context = {
		'deals': dealsmodule.get_deals(),
		'recommendations': restaurant_module.get_favorites_using_user_ID(),
		'recent_orders': restaurant_module.get_recent_using_user_ID(request.session['ID']),
		'user_authenticated': request.session['is_authenticated']
	}
	# If not logged in, go to home page instead
	return render(request, 'dumpApp/dashboard.html', context)

def shopping_cart(request):
	check_user(request)

	if request.session['is_authenticated'] == False:
		return redirect('login')

	context = {
		'user_authenticated': request.session['is_authenticated'],
	}
	context['shopping_cart'] = request.session['shopping_cart']
	order_object = order_module.order_list(request.session['ID'], 5, 0)
	order_object.create_from_dict_list(request.session['shopping_cart'])
	context['shopping_cart_subtotal']=order_object.get_order_subtotal()

	return render(request, 'dumpApp/shopping_cart.html', context)

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
		name = request.POST['myvalue']
		
	context['search_results_db'] = restaurant_module.get_restaurant_using_keyword(request.POST['myvalue'])
	print(context['search_results_db'])

	try:
		radius = request.POST['myRadius']
		price = request.POST['myPrice']
	except :
		radius = "1000"
		price = "1, 2, 3, 4"

	
	context['search_results'] = YelpFusion.search_yelp(term = request.POST['myvalue'], location = request.POST['locationValue'], radius = radius, price= price)

	return render(request, 'dumpApp/search_results.html', context)


def get_query_results(query=None):
	queryset = []
	#creating a list out of all the query phrases
	#so queries is a list
	queries = query.split("")
	for q in queries:
		posts = BlogPost.objects.filter(
				Q(title__icontains=q) |
				Q(body__icontains=q)
			).distinct()
		for post in posts:
			queryset.append(post)

	return list(set(queryset))


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
		request.session['preferences'] = user.other_info
		request.session['is_authenticated'] = user.is_authenticated
		print("Before creating order_list")
		order_object = order_module.order_list(user.ID, 2, 0)
		print("After creating order_list")


		request.session['shopping_cart'] = order_object.convert_to_dict_list()

		request.session['current_item'] = dict(description='', item_price='', item_image='', item_name='', item_ID='', menu_ID='', restaurant_ID='', item_quantity='')

		print(request.session['is_authenticated'])
		context['user_authenticated'] = request.session['is_authenticated']
		context['recommendations'] = restaurant_module.get_favorites_using_user_ID()
		context['recent_orders'] = restaurant_module.get_recent_using_user_ID(request.session['ID'])
		context['deals'] = dealsmodule.get_deals()
		request.session['is_authenticated'] = True
		return redirect('dashboard')
	except:
		print("There is an error")
		context['error'] = "Invalid username or password"
		return render(request, 'dumpApp/login.html', context)

def register(request):
	check_user(request)
	if request.session['is_authenticated'] == True:
		return redirect('dashboard')
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
	if request.session['is_authenticated'] == False:
		return redirect("login")

	order_history = order_module.getOrderHistory(request.session['ID'])

	if request.method == "POST":
		context = {
			'user_authenticated': request.session['is_authenticated'],
			'email': request.session['email'],
			'phone': request.session['cell'],
			'username': request.session['username'],
			'payment_option': request.session['payment_option'],
			'photo': request.session['photo'],
			'preferences': request.session['preferences'],
			'order_history': order_history,
		}

		review_ID = review_module.writeReview(request.POST['Restaurant_ID'], request.POST['Order_ID'], request.POST['User_ID'], request.POST['star'], request.POST['review_text'])

		context['reviews'] = review_module.getReview(request.session['ID'])

		return render(request, 'dumpApp/profile.html', context)
	
	context = {
		'user_authenticated': request.session['is_authenticated'],
		'email': request.session['email'],
		'phone': request.session['cell'],
		'username': request.session['username'],
		'payment_option': request.session['payment_option'],
		'photo': request.session['photo'],
		'preferences': request.session['preferences'],
		'order_history': order_history,
	}
	context['reviews'] = review_module.getReview(request.session['ID'])


	return render(request, 'dumpApp/profile.html', context)

def restaurants(request):
	check_user(request)

	#the dictionary context is the database query
	context = {}
	context['user_authenticated'] = request.session['is_authenticated']
	

	if request.method == "POST":

		print(request.POST['Yelp'])
		if request.POST['Yelp'] == "True":
			restaurant = YelpFusion.search_restaurant(request.POST['id'])
			context['everything'] = restaurant

			schedule = {}
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

			restaurant = restaurant_module.get_restaurant_using_ID(request.POST['id'])
			context['restaurants'] = restaurant[0]

			restaurant_location = restaurant_module.get_location_using_location_id(restaurant[0]['Location_id'])
			context['rest_address'] = restaurant_location[0]

			items = restaurant_module.get_menu_items_using_restaurant_ID(request.POST['id'])
			context['rest_items'] = items



			#get the reviews

			context['reviews'] = review_module.get_reviews_by_restaurant_ID(request.POST['id'])

	return render(request, 'dumpApp/restaurants.html', context)


def item(request):
	check_user(request)
	context = {}
	if request.method == "POST":
		if request.session['is_authenticated'] == False:
			return redirect('login')
		if request.POST['origin'] == "item":
			quantity = request.POST['item_quantity']
			request.session['current_item']['item_quantity'] = quantity


			# #start --- FOR TESTING
			# #create a new order item to add to the list
			order_object = order_module.order_list(request.session['ID'], 0, 0)
			order_object.create_from_dict_list(request.session['shopping_cart'])


			order_object.add_item_by_ID(request.session['current_item']['item_ID'], request.session['current_item']['item_quantity'])

			request.session['shopping_cart'] = order_object.convert_to_dict_list()


			# #end --- FOR TESTING

		elif request.POST['origin'] == "dashboard":
			print(request.POST.get('dic', False))
			description = request.POST['description']
			price = request.POST['price']
			image = request.POST['image']
			caption = request.POST['caption']
			item_id = request.POST['item_ID']
			menu_id = request.POST['menu_ID']
			restaurant_id = request.POST['restaurant_ID']

			request.session['current_item']['description'] = description
			request.session['current_item']['item_price'] = price
			request.session['current_item']['item_image'] = image
			request.session['current_item']['item_name'] = caption
			request.session['current_item']['item_ID'] = item_id
			request.session['current_item']['menu_ID'] = menu_id
			request.session['current_item']['restaurant_ID'] = restaurant_id



		context = {
		'current_item': request.session['current_item'],
		'shopping_cart':request.session['shopping_cart'],
		'dic':request.POST.get('dic', False),
		'user_authenticated': request.session['is_authenticated']
	}
	return render(request, 'dumpApp/item.html', context)

def checkout(request):
	check_user(request)
	if request.session['is_authenticated'] == False:
		return redirect('login')

	context = {
	'shopping_cart': request.session['shopping_cart'],
	'user_authenticated': request.session['is_authenticated']
	}
	order_object = order_module.order_list(request.session['ID'], 0, 0)
	order_object.create_from_dict_list(request.session['shopping_cart'])
	request.session['shopping_cart'] = order_object.convert_to_dict_list()
	context['shopping_cart_subtotal']=order_object.get_order_subtotal()
	context['shopping_cart_tax']=order_object.get_order_subtotal()*0.1
	context['shopping_cart_total']=order_object.get_order_total()

	return render(request, 'dumpApp/checkout.html', context)

def checkout_success(request):
	check_user(request)
	if request.session['is_authenticated'] == False:
		return redirect('login')
	order_object = order_module.order_list(request.session['ID'], 2, 1)
	order_object.create_from_dict_list(request.session['shopping_cart'])
	order_object.submit()

	#clearing the shopping cart
	order_object_empty = order_module.order_list(request.session['ID'], 0, 0)
	request.session['shopping_cart'] = order_object_empty.convert_to_dict_list()

	context = {
	'shopping_cart': request.session['shopping_cart'],
	'user_authenticated': request.session['is_authenticated']
	}
	return render(request, 'dumpApp/checkout_success.html', context)
