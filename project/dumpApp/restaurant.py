import DBSetup
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
		ret = list()
		for rest in output:
			ret.append(dict(ID=rest[0], Name=rest[1], Location_ID=rest[2], Category=rest[3], Cuisine=rest[4], Notes=rest[5], Image=rest[6]))
		return ret

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
		query = "SELECT * FROM Restaurant WHERE Restaurant_name LIKE '%" + str(keyword) + "%';"
		cursor.execute(query)
		output = cursor.fetchall()
		cursor.close()
		conn.close()
		ret = list()
		for rest in output:
			ret.append(dict(ID=rest[0], Name=rest[1], Location_ID=rest[2], Category=rest[3], Cuisine=rest[4], Notes=rest[5], Image=rest[6]))
		return ret


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
		print(str(ID))
		cursor = conn.cursor()
		query = "SELECT Item_name, Item_cost, item_notes, item_image FROM Restaurant R INNER JOIN Menu M ON R.Restaurant_ID=M.Restaurant_ID "
		query += "INNER JOIN Item I ON M.Menu_ID = I.Menu_ID "
		query += "WHERE R.Restaurant_ID = " + str(ID) + " ; "
		cursor.execute(query)
		output = cursor.fetchall()
		ret = list()
		for rest in output:
			ret.append(dict(Name=rest[0], Cost=rest[1], Notes=rest[2], Image=rest[3]))

		return ret


#get_restaurant_using_ID(7)
#get_restaurant_using_keyword('pizza')
#get_menu_items_using_restaurant_ID(9)
#print(get_recent_using_user_ID(1))
#print(get_favorites_using_user_ID(1))
