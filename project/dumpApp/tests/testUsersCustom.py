from django.test import SimpleTestCase
from . import DBSetup
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
			query = "DELETE FROM Users WHERE User_Email = 'test@test.com';"	
			cursor.execute(query)
			query = "DELETE FROM Users WHERE User_Email = 'testtest@test.com';"	
			cursor.execute(query)
			conn.commit()	#clear test values
			self.assertEqual(usersCustom.create_user("test@test.com","testPassword","testName","testCell"),True)	#test create_user
			u = usersCustom.authenticate_user("test@test.com", "testPassword")	#test authenticate_user
			query = "SELECT * FROM Users WHERE User_Email=\"test@test.com\";"
			cursor.execute(query)
			fetchedList = cursor.fetchall()
			fetchedUser = usersCustom.userC(fetchedList[0])
			self.assertEqual(u.get_dictionary(),fetchedUser.get_dictionary())
			modifiedDictionary = fetchedUser.get_dictionary()	#test userC.save_preferences
			modifiedDictionary['email'] = "testtest@test.com"
			u.save_preferences(that_dict=modifiedDictionary)
			v = usersCustom.authenticate_user("testtest@test.com","testPassword")
			self.assertEqual((u.get_dictionary())['email'],(v.get_dictionary())['email'])
			u.logout()		#test ucerC.logout
			self.assertEqual(u.is_authenticated, False)


			query = "DELETE FROM Users WHERE User_Email = 'test@test.com';"	#delete test values
			cursor.execute(query)
			query = "DELETE FROM Users WHERE User_Email = 'testtest@test.com';"	
			cursor.execute(query)
			conn.commit()
			cursor.close()
			conn.close()