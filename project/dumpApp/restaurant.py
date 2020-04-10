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
		cursor = conn.cursor()
		query = "SELECT * FROM Restaurant WHERE Restaurant_id =" + str(ID) + ";"
		cursor.execute(query)
		output = cursor.fetchall()
		cursor.close()
		conn.close()
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
		cursor = conn.cursor()
		query = "SELECT * FROM Item_name, Item_cost, item_notes, item_image WHERE Menu_id LIKE '%" + str(keyword) + "%';"
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
		cursor = conn.cursor()
		query = "SELECT Item_name, Item_cost, item_notes, item_image FROM Restaurant R INNER JOIN Menu M ON R.Restaurant_ID=M.Restaurant_ID "
		query += "INNER JOIN Item I ON M.Menu_ID = I.Menu_ID " 
		query += "WHERE R.Restaurant_ID = " + str(ID) + " ; "
		cursor.execute(query)
		output = cursor.fetchall()
		cursor.close()
		conn.close()
		return output


#get_restaurant_using_ID(7)
#get_restaurant_using_keyword('Restaurant')
#get_menu_items_using_restaurant_ID(9)