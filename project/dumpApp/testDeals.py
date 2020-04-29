from django.test import SimpleTestCase
from . import DBSetup
from . import deals


class TestDeals(SimpleTestCase):

	def test_get_deals_1(self):
		#tests the correct format list of dicts
		self.assertEqual(deals.get_deals(), [{'Price': 12.49, 'Name': 'Pad Thai', 'Image': 'https://www.feastingathome.com/wp-content/uploads/2016/04/easy-authentic-pad-thai-recipe-100.jpg', 'Restaurant_Name': 'Crispy Pork Gang Restaurant', 'Menu_ID': 11, 'Item_ID': 31, 'Restaurant_ID': 8}])
		return

	def test_get_deals_2(self):
		#tests the components of deals
		test = deals.get_deals()[0]

		self.assertIn('Price' , test)
		self.assertIn('Name' , test)
		self.assertIn('Image' , test)
		self.assertIn('Restaurant_Name' , test)
		self.assertIn('Menu_ID' , test)
		self.assertIn('Item_ID' , test)
		self.assertIn('Restaurant_ID' , test)
		return

