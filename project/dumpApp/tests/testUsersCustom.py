from django.test import SimpleTestCase
from dumpApp import DBSetup
from dumpApp import usersCustom
import mysql.connector
from mysql.connector import errorcode
from django.contrib.auth.hashers import check_password, make_password

#python manage.py test dumpapp.tests.testUsersCustom
class usersCustomTestCase(SimpleTestCase):
	#userC_test(ID, payment_option, username, email, passwordENC, cell, photoURL, gender, other_info, is_authenticated):
	#create_user(email, passwordPLAIN, username, cellPhoneNum):
	#authenticate_user(email, passwordPLAIN):
	def testUsersCustomFunctions(self):
		config = DBSetup.setup_config()
		try:
			conn = mysql.connector.connect(**config)
			print("Connection established")
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with the user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)
		else: 
			cursor = conn.cursor(dictionary = True)
			self.assertEqual(usersCustom.create_user("test@test.com","testPassword","testName","testCell"),True)
			u = usersCustom.authenticate_user("test@test.com", "testPassword")
			print(u.get_dictionary())
			self.assertEqual(u.get_dictionary(),{'username': 'testName', 'locationID': None, 'paymentOption': None, 'email': 'test@test.com', 'password': 'pbkdf2_sha256$180000$ObAKOy5FmYqk$KjE1tjcnpAw5uHJwdXQY4uCiivwSw369A7nzVMpu3xc=', 'cellPhoneNumber': 'testCell', 'preferences': None, 'photo': None, 'gender': None})
			#the code writes a new hash each time the test user is created, so having these values will not work. need to get them off of the the server, instead.




			query = "DELETE FROM Users WHERE User_Email = 'test@test.com';"
			cursor.execute(query)
			conn.commit()
			cursor.close()
			conn.close()