from django.shortcuts import render
from personal.models import Question

deals = [
	{
		'name': 'Deal 1',
		'food_type': 'Deal Type 1',
		'restaurant': 'Restaurant 1',
		'price': '$11',
		'rating': '4.5 Stars',
		'is_saved': 'false',
		'duration': '20-30 min',
		'items': 'item_1',
	},
	{
		'name': 'Deal 2',
		'food_type': 'Deal Type 2',
		'restaurant': 'Restaurant 2',
		'price': '$22',
		'rating': '3 Stars',
		'ss_saved': 'true',
		'duration': '30-35 min',
		'items': 'item_2',
		}
]

def home_screen_view(request):
    #context = {
	#	'deals': deals
    #}
	#inconsistent use of tabs and spaces???
	#context['number'] = 222
	#context = {
	#	'deals': deals,
	#	'some_string': "this is some string",
	#	'some_number': 22,
	#}

	# context = {}
	# list_of_values = []
	# list_of_values.append("first entry")
	# list_of_values.append("second entry")
	# list_of_values.append("third entry")
	# list_of_values.append("forth entry")
	# context['list_of_values'] = list_of_values


	#selecting all the question objects (rows) from the database
	questions = Question.objects.all()
	context = {}
	context['questions'] = questions

	return render(request, "personal/home.html", context)
