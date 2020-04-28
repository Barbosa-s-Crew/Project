from django.test import TestCase
from . import DBSetup
from . import usersCustom

class usersCustomTestCase(TestCase):
	def userC_test(ID, payment_option, username, email, passwordENC, cell, photoURL, gender, other_info, is_authenticated):
		return

	def create_user_test(email, passwordPLAIN, username, cellPhoneNum):
		return

	def authenticate_user_test(email, passwordPLAIN):
		return
