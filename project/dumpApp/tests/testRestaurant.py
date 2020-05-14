from django.test import SimpleTestCase
from dumpApp import DBSetup
from dumpApp import restaurant
import datetime
#python manage.py test dumpapp.testRestaurant
class restaurantTestCase(SimpleTestCase):	
	#def get_restaurant_orders(ID):
	def test_restaurant_functions(self):
		
		u = restaurant.get_restaurant_using_ID(7)
		self.assertEqual(u[0],dict(Restaurant_id=7, Restaurant_name='Cajun Seafood House',Location_id=2,Restaurant_Category='2', Restaurant_Cuisine=None, Restaurant_Notes=None, Restaurant_photo='https://media-cdn.tripadvisor.com/media/photo-s/07/97/d6/3c/cajun-house.jpg'))
		
		
		u= restaurant.get_restaurant_using_keyword('Seafood')
		self.assertEqual(u[0],dict(Restaurant_id=7, Restaurant_name='Cajun Seafood House',Location_id=2,Restaurant_Category='2', Restaurant_Cuisine=None, Restaurant_Notes=None, Restaurant_photo='https://media-cdn.tripadvisor.com/media/photo-s/07/97/d6/3c/cajun-house.jpg'))
		
		
		u = restaurant.get_menu_items_using_restaurant_ID(4)
		self.assertEqual(u,[{'Item_name': 'Item 7', 'Item_cost': 29.0, 'item_notes': None, 'item_image': None}, {'Item_name': 'Item 7', 'Item_cost': 29.0, 'item_notes': None, 'item_image': None}, {'Item_name': 'Item 7', 'Item_cost': 29.0, 'item_notes': None, 'item_image': None}])
		

		u = restaurant.get_favorites_using_user_ID(1)
		self.assertEqual(u, [{'Restaurant_id': 11, 'Restaurant_name': 'Pizza and Panini Party', 'Location_id': 2, 'Restaurant_Category': '2', 'Restaurant_Cuisine': None, 'Restaurant_Notes': None, 'Restaurant_photo': 'https://assets.bwbx.io/images/users/iqjWHBFdfxIU/im.i99yGmzLo/v0/1000x-1.jpg'}, {'Restaurant_id': 10, 'Restaurant_name': "India's Restaurant", 'Location_id': 2, 'Restaurant_Category': '2', 'Restaurant_Cuisine': None, 'Restaurant_Notes': None, 'Restaurant_photo': 'https://media-cdn.tripadvisor.com/media/photo-s/03/26/0e/b1/india-s-restaurant.jpg'}, {'Restaurant_id': 9, 'Restaurant_name': 'Bamboo Chinese Cuisine', 'Location_id': 2, 'Restaurant_Category': '2', 'Restaurant_Cuisine': None, 'Restaurant_Notes': None, 'Restaurant_photo': 'https://lh5.googleusercontent.com/p/AF1QipNcuo8I0M1S4l3y8Xed6UT5bD1oi5vhELK1M5t_=w426-h240-k-no'}, {'Restaurant_id': 8, 'Restaurant_name': 'Crispy Pork Gang Restaurant', 'Location_id': 1, 'Restaurant_Category': '1', 'Restaurant_Cuisine': None, 'Restaurant_Notes': None, 'Restaurant_photo': 'https://2.bp.blogspot.com/-MXGm_KeIu-0/TrNGbctp2fI/AAAAAAAACdU/wGpNS9ONd7M/s1600/DSCN9853.JPG'}, {'Restaurant_id': 7, 'Restaurant_name': 'Cajun Seafood House', 'Location_id': 2, 'Restaurant_Category': '2', 'Restaurant_Cuisine': None, 'Restaurant_Notes': None, 'Restaurant_photo': 'https://media-cdn.tripadvisor.com/media/photo-s/07/97/d6/3c/cajun-house.jpg'}, {'Restaurant_id': 6, 'Restaurant_name': 'Rest 5', 'Location_id': 5, 'Restaurant_Category': '5', 'Restaurant_Cuisine': None, 'Restaurant_Notes': None, 'Restaurant_photo': ''}, {'Restaurant_id': 5, 'Restaurant_name': 'Rest 4', 'Location_id': 4, 'Restaurant_Category': '4', 'Restaurant_Cuisine': None, 'Restaurant_Notes': None, 'Restaurant_photo': ''}, {'Restaurant_id': 4, 'Restaurant_name': 'Rest 3', 'Location_id': 3, 'Restaurant_Category': '3', 'Restaurant_Cuisine': None, 'Restaurant_Notes': None, 'Restaurant_photo': ''}, {'Restaurant_id': 3, 'Restaurant_name': 'Rest 2', 'Location_id': 2, 'Restaurant_Category': '2', 'Restaurant_Cuisine': None, 'Restaurant_Notes': None, 'Restaurant_photo': ''}, {'Restaurant_id': 2, 'Restaurant_name': 'Rest 1', 'Location_id': 1, 'Restaurant_Category': '1', 'Restaurant_Cuisine': None, 'Restaurant_Notes': None, 'Restaurant_photo': ''}])
		

		u = restaurant.get_recent_using_user_ID(1)
		self.assertNotEqual(u,[])


		u = restaurant.get_restaurant_orders(3)
		self.assertNotEqual(u,[])
		

		u = restaurant.get_location_using_location_id(2)
		self.assertEqual(u[0],dict(Location_ID=2,Location_Street_1='222 Milford Street',Location_Street_2='Suit 200',Location_City='Glendale',Location_State='CA',Location_Zip=None,Location_Longitude='80.222',Location_Latitude='34.222',API=None))
