from . import DBSetup
import mysql.connector
from mysql.connector import errorcode

def get_restaurant_using_ID(ID = 0):
	config = DBSetup.setup_config()
	# Construct connection string
	try:
		conn = mysql.connector.connect(**config)
		#print("Connection established")
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with the user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cursor = conn.cursor(dictionary = True)
		query = "SELECT * FROM Restaurant WHERE Restaurant_id = \""+str(ID)+"\";"
		cursor.execute(query)
		output = cursor.fetchall()
		cursor.close()
		conn.close()
		ret = list()
		return output

def get_restaurant_using_keyword(keyword = ''):
	config = DBSetup.setup_config()
	# Construct connection string
	try:
		conn = mysql.connector.connect(**config)
		#print("Connection established")
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with the user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		keywordList = keyword.split()
		#keywordList = [ '%{0}%'.format(element) for element in keywordList ]
		cursor = conn.cursor(dictionary = True)
		#print(len(keywordList))
		if len(keywordList) > 0:
			query = "SELECT * FROM Restaurant WHERE Restaurant_name LIKE \"%"+keywordList[0]+"%\""
			if len(keywordList) > 1:
				for x in range(len(keywordList)-1):
					query += " OR Restaurant_name LIKE \"%"+keywordList[x+1]+"%\""
			query += ";"
			#print(query)
			cursor.execute(query)
			output = cursor.fetchall()
			cursor.close()
			conn.close()
			return output


def get_menu_items_using_restaurant_ID(ID = 0):
	config = DBSetup.setup_config()
	# Construct connection string
	try:
		conn = mysql.connector.connect(**config)
		#print("Connection established")
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with the user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		#print(str(ID))
		cursor = conn.cursor(dictionary = True)
		query = "SELECT Item_name, Item_cost, item_notes, item_image FROM Restaurant R INNER JOIN Menu M ON R.Restaurant_ID=M.Restaurant_ID "
		query += "INNER JOIN Item I ON M.Menu_ID = I.Menu_ID "
		query += "WHERE R.Restaurant_ID = \""+str(ID)+"\"; "
		cursor.execute(query)
		output = cursor.fetchall()
		cursor.close()
		conn.close()
		return output

def get_favorites_using_user_ID(ID=0):	#using dumb query, needs updating
	config = DBSetup.setup_config()
	# Construct connection string
	try:
		conn = mysql.connector.connect(**config)
		#print("Connection established")
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with the user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cursor = conn.cursor(dictionary = True)
		query = "SELECT * FROM Restaurant ORDER BY Restaurant_id DESC LIMIT 10;"
		cursor.execute(query)
		output = cursor.fetchall()
		cursor.close()
		conn.close()
		ret = list()
		return output

def get_recent_using_user_ID(ID=0):
	config = DBSetup.setup_config()
	# Construct connection string
	try:
		conn = mysql.connector.connect(**config)
		#print("Connection established")
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with the user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cursor = conn.cursor(dictionary = True)
		query = "SELECT * FROM Orders WHERE User_ID = \""+str(ID)+"\" ORDER BY Order_start_time DESC LIMIT 10;"
		cursor.execute(query)
		output = cursor.fetchall()
		cursor.close()
		conn.close()
		return output

def get_location_using_location_id(ID=0):
	config = DBSetup.setup_config()
	try:
		conn = mysql.connector.connect(**config)
		#print("Connection established")
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with the user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cursor = conn.cursor(dictionary = True)
		query = "SELECT * FROM Location WHERE Location_ID = \""+str(ID)+"\";"
		cursor.execute(query)
		output = cursor.fetchall()
		return output

def get_restaurant_orders(ID=0):
	config = DBSetup.setup_config()
	try:
		conn = mysql.connector.connect(**config)
		#print("Connection established")
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with the user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cursor = conn.cursor(dictionary = True)
		query = "SELECT * FROM Order_items WHERE Restaurant_ID = \""+ str(ID) +"\";"
		cursor.execute(query)
		output = cursor.fetchall()
		cursor.close()
		conn.close()
		return output

#r = get_restaurant_using_ID(7)
#r = get_restaurant_using_keyword("a")
#r = get_menu_items_using_restaurant_ID(9)
#r = get_recent_using_user_ID(1)
#r = get_location_using_location_id(1)
#r = get_favorites_using_user_ID(1)
#r = get_restaurant_orders(1)
#print(r)
#print(len(r))