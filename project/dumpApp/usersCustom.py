import mysql.connector
from mysql.connector import errorcode
from . import DBSetup
from django.contrib.auth.hashers import check_password, make_password

#User_ID int not null identity,
#    Location_ID int,
#    Payment_Option_ID int,
#    User_name varchar(40) not null,
#    User_Email varchar(60),
#    User_Password varchar(255) not null,
#    User_Cell varchar(14),
#    Other_Information text,

class userC:
	ID = ''
	Location_ID = ''
	payment_option = ''
	username = ''
	email = ''
	password = ''
	cell = ''
	photoURL = ''
	gender = ''
	other_info = ''
	is_authenticated = False

	def __init__(self, tup):
		try:
			self.ID = tup[0]
			self.Location_ID = tup[1]
			self.payment_option = tup[2]
			self.username = tup[3]
			self.email = tup[4]
			self.password = tup[5]
			self.cell = tup[6]
			self.photoURL = tup[7]
			self.gender = tup[8]
			self.other_info = tup[9]
		
			#tup is not empty
			if tup[0] != '':
				self.is_authenticated = True
		except:
			self.ID = ''
			self.Location_ID = ''
			self.payment_option = ''
			self.username = ''
			self.email = ''
			self.password = ''
			self.cell = ''
			self.photoURL = ''
			self.gender = ''
			self.other_info = ''
			self.is_authenticated = False

	def logout(self):
		self.ID = ''
		self.payment_option = ''
		self.username = ''
		self.email = ''
		self.password = ''
		self.cell = ''
		self.other_info = ''
		self.is_authenticated = False

	def get_dictionary(self):
		print(self.username)
		this_dict = dict(username = self.username, locationID = self.Location_ID, paymentOption = self.payment_option, email=self.email, password = self.password, cellPhoneNumber = self.cell, preferences = self.other_info, photo=self.photoURL, gender=self.gender)
		print(self.email)
		return this_dict

	def save_preferences(self, that_dict):		#use make_password before saving the settings, convert commas in the preferences string to "&&"
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
			oldEmail = self.email
			self.username = that_dict.get("username")
			self.email = that_dict.get("email")
			self.password = that_dict.get("password")
			self.cell = that_dict.get("cellPhoneNumber")
			self.other_info = that_dict.get("preferences")
			self.photoURL = that_dict.get("photo")
			self.gender = that_dict.get("gender")
			#self.Location_ID = that_dict.get("locationID")
			#self.payment_option = that_dict.get("paymentOption")
			cursor = conn.cursor(prepared = True)
			query_tuple = (self.username, self.email, self.password, self.cell, self.photoURL, self.gender, self.other_info, oldEmail)
			query = "UPDATE Users SET User_name = ?,User_Email = ?,User_Password = ?,User_Cell = ?,user_image = ?, user_gender =?, Other_Information = ? WHERE User_Email= ?"
			cursor.execute(query, query_tuple)
			conn.commit()
			conn.close()




def authenticate_user(email='', password = ''):
	output = ""
	# Obtain connection string information from the portal
	config = DBSetup.setup_config()

		# Construct connection string
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
		cursor = conn.cursor(prepared = True)
		query = "SELECT * FROM Users WHERE User_Email=?"
		email_tuple = (email,)
		cursor.execute(query, email_tuple)
		tupleC = cursor.fetchall()
		fetchedUser = userC(tupleC[0])
		cursor.close()
		conn.close()
		if check_password(password, fetchedUser.password):
			print("Valid email/password combination.")
			return fetchedUser
		else:
			print("No valid email/password combination found.")
				
def create_user(email = '', password = '',username='',cellPhoneNum=''):		#will return true if an account can be made, otherwise will return false
	config = DBSetup.setup_config()
	result = False

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
		cursor = conn.cursor(prepared = True)
		query = "SELECT * FROM Users WHERE User_Email= ?"
		email_tuple = (email,)
		cursor.execute(query, email_tuple)
		tupleC = cursor.fetchall()
		if len(tupleC)==0:
			query = "INSERT INTO Users (User_name, User_Email, User_Password, User_Cell) VALUES (?, ?, ?, ?);"
			query_tuple = (username, email, make_password(password), cellPhoneNum)
			cursor.execute(query, query_tuple)
			conn.commit()
			conn.close()
			result = True
			print('User Created')

		else: 
			print("A user with that email already exists.")
			cursor.close()
			conn.close()
		return result



#create_user(email = 'GGG', password = '123')	#this one probably doesn't work anymore.

#u=authenticate_user(username='abc',password= '123')
#create_user('jikemsa@gmail.com','jikemsaPassword','Hunter Swanson','(408)507-0461')
#u=authenticate_user('jikemsa@gmail.com','jikemsaPassword')
#a=u.get_dictionary()
#print(a)
#a.update({"username":"Hunter Swanson"})
#print(a)
#u.save_preferences(a)
#u=authenticate_user('jikemsa@gmail.com','jikemsaPassword')
#a=u.get_dictionary()
#print(a)