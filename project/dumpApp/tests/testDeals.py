from django.test import SimpleTestCase
from . import DBSetup
from dumpApp import deals


class TestDeals(SimpleTestCase):

	def test_get_deals_1(self):
		#tests the correct format list of dicts
		self.assertEqual(deals.get_deals(), [])
		return

	def test_get_deals_2(self):
		#tests the components of deals
		test = deals.get_deals()
		
		self.assertEqual(test, [])
		return

