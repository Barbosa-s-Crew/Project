import mysql.connector
from mysql.connector import errorcode
#import encryption
from . import DBSetup

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
	

def authenticate_user(username='', password = ''):
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
		cursor.execute("SELECT * FROM users WHERE User_Email='"+username+"'")
		tupleC = cursor.fetchall()
		#print(tupleC[0])
		fetchedUser = userC(tupleC[0])
		cursor.close()
		conn.close()
		print(fetchedUser.password)
		#newKey = encryption.verify(password, fetchedUser.password)
		#print(newKey)
		#if newKey == fetchedUser.password:
		if password == fetchedUser.password:
			print("Valid email/password combination.")
			return fetchedUser
		else:
			print("No valid email/password combination found.")
			#return userC()
				
def create_user(email = '', password = ''):
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
		#cursor.execute("INSERT INTO users (User_ID, Payment_Option_ID, User_name, User_Email, User_Password, User_Cell, Other_Information) VALUES ('"+user.ID+"', '"+user.payment_option+"',  '"+user.username+"', '"+user.password+"', '"+user.Cell+"', '"+user.other_info+"')")
		#cursor.execute("INSERT INTO users (User_Email, User_Password) VALUES ('"+email+"', '"+str(encryption.encrypt(password)).replace('\\', '\\\\').replace('\'','\\\'').replace('\"','\\\"') +"');")
		cursor.execute("INSERT INTO users (User_Email, User_Password) VALUES ('"+email+"', '"+password+"');")
		#print("INSERT INTO users (User_Email, User_Password) VALUES ('"+email+"', '"+str(encryption.encrypt(password)).replace('\\', '\\\\').replace('\'','\\\'').replace('\"','\\\"') +"');")
		conn.commit()
		cursor.close()
		conn.close()

#create_user(email = 'GGG', password = '123')

u = authenticate_user(username = 'thomas97@gmail.com', password = 'thomaspassword')


#print(u.ID)
