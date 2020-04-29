from django.test import TestCase
from . import DBSetup
from . import deals


class DealsTestCase(TestCase):

	def get_deals_test(self):
		
		self.assertEqual(deals.get_deals(), [])
		return

	def format_deals_test(self, listOTuples):
		return
print("here")
print(deals.get_deals())
