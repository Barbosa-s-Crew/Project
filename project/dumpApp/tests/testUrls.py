from django.test import SimpleTestCase
from django.urls import reverse, resolve
from dumpApp.views import  home, search, about, dump, browse, deals, order, search_results, shopping_cart, login, register, login_error, profile, logout, restaurants, item, checkout, checkout_success, dashboard



 
class TestUrls(SimpleTestCase):

	def test_home_url_resolves(self):
		url = reverse('home')
		self.assertEquals(resolve(url).func, home)
		

	def test_search_url_resolves(self):
		url = reverse('search')
		self.assertEquals(resolve(url).func, search)


	def test_about_url_resolves(self):
		url = reverse('about')
		self.assertEquals(resolve(url).func, about)

	def test_dump_url_resolves(self):
		url = reverse('dump')
		self.assertEquals(resolve(url).func, dump)

	def test_browse_url_resolves(self):
		url = reverse('browse')
		self.assertEquals(resolve(url).func, browse)

	def test_deals_url_resolves(self):
		url = reverse('deals')
		self.assertEquals(resolve(url).func, deals)
		#WE DON'T USE IT
		
	def test_order_url_resolves(self):
		url = reverse('order')
		self.assertEquals(resolve(url).func, order)

	def test_search_results_url_resolves(self):
		url = reverse('search_results')
		self.assertEquals(resolve(url).func, search_results)

	def test_shopping_cart_url_resolves(self):
		url = reverse('shopping_cart')
		self.assertEquals(resolve(url).func, shopping_cart)

	def test_login_url_resolves(self):
		url = reverse('login')
		self.assertEquals(resolve(url).func, login)

	def test_register_url_resolves(self):
		url = reverse('register')
		self.assertEquals(resolve(url).func, register)

	def test_login_error_url_resolves(self):
		url = reverse('login_error')
		self.assertEquals(resolve(url).func, login_error)

	def test_profile_url_resolves(self):
		url = reverse('profile')
		self.assertEquals(resolve(url).func, profile)

	def test_logout_url_resolves(self):
		url = reverse('logout')
		self.assertEquals(resolve(url).func, logout)

	def test_restaurants_url_resolves(self):
		url = reverse('restaurants')
		self.assertEquals(resolve(url).func, restaurants)

	def test_item_url_resolves(self):
		url = reverse('item')
		self.assertEquals(resolve(url).func, item)

	def test_checkout_url_resolves(self):
		url = reverse('checkout')
		self.assertEquals(resolve(url).func, checkout)

	def test_checkout_success_url_resolves(self):
		url = reverse('checkout_success')
		self.assertEquals(resolve(url).func, checkout_success)

	def test_dashboard_url_resolves(self):
		url = reverse('dashboard')
		self.assertEquals(resolve(url).func, dashboard)

 #    path('dashboard/', views.dashboard, name='dashboard'),