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
		ID = tup['User_ID']
		payment_option = tup['Payment_Option_ID']
		username = tup['User_name']
		email = tup['User_Email']
		password = tup['User_Password']
		cell = tup['User_Cell']
		other_info = tup['Other_Information']

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
		tuple = cursor.fetchall()
		for field in tuple:
			print(field)

		cursor.close()
		conn.close()
		return tuple


authenticate_user(username = 'thomas97@gmail.com', password = 'thomaspassword')