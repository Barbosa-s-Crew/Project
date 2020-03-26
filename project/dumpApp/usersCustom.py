import mysql.connector
from mysql.connector import errorcode
from . import DBSetup
from django.contrib.auth.hashers import check_password, make_password

class userC:
	ID = ''
	payment_option = ''
	username = ''
	email = ''
	password = ''
	cell = ''
	other_info = ''
	is_authenticated = False

	def __init__(self, tup):
		try:
			self.ID = tup[0]
			self.payment_option = tup[1]
			self.username = tup[2]
			self.email = tup[3]
			self.password = tup[4]
			self.cell = tup[5]
			self.other_info = tup[6]
		
			#tup is not empty
			if tup[0] != '':
				self.is_authenticated = True
		except:
			self.ID = ''
			self.payment_option = ''
			self.username = ''
			self.email = ''
			self.password = ''
			self.cell = ''
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
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM users WHERE User_Email='"+email+"'")
		tupleC = cursor.fetchall()
		fetchedUser = userC(tupleC[0])
		cursor.close()
		conn.close()
		if check_password(password, fetchedUser.password):
			print("Valid email/password combination.")
			return fetchedUser
		else:
			print("No valid email/password combination found.")
				
def create_user(email = '', password = ''):		#will return true if an account can be made, otherwise will return false
	config = DBSetup.setup_config()
	result = False
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
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM users WHERE User_Email='"+email+"'")
		tupleC = cursor.fetchall()
		if len(tupleC)==0:
			cursor.execute("INSERT INTO users (User_Email, User_Password) VALUES ('"+email+"', '"+make_password(password)+"');")
			conn.commit()
			result = True
		else: 
			print("A user with that email already exists.")
		cursor.close()
		conn.close()
		return result

#create_user(email = 'GGG', password = '123')	#this one probably doesn't work anymore.

#u=authenticate_user(username='abc',password= '123')
#create_user('jikemsa@gmail.com','jikemsaPassword')
#u=authenticate_user('jikemsa@gmail.com','jikemsaPassword')

#print(u.email)
