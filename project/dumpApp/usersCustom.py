import mysql.connector
from mysql.connector import errorcode

class userC:
	ID = ''
	payment_option = ''
	username = ''
	email = ''
	password = ''
	cell = ''
	other_info = ''

	def __init__(self, tup):
		self.ID = tup[0]
		self.payment_option = tup[1]
		self.username = tup[2]
		self.email = tup[3]
		self.password = tup[4]
		self.cell = tup[5]
	#other_info = tup[6]

def authenticate_user(username='', password = ''):
	output = ""
	# Obtain connection string information from the portal
	config = {
	'host':'barbosascrew.mysql.database.azure.com',
	'user':'BarbosasCrew@barbosascrew',
	'password':'Glendale2020',
	'database':'application database'
	}

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
		cursor.execute("SELECT * FROM users WHERE User_Email='"+username+"' AND User_Password='"+password+"'")
		tupleC = cursor.fetchall()
		#print(tupleC[0])

		cursor.close()
		conn.close()
		return userC(tupleC[0])


u = authenticate_user(username = 'thomas97@gmail.com', password = 'thomaspassword')

print(u.ID)