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
		keywordList = keyword.split()
		cursor = conn.cursor()
		keywordList = [word.replace("\'","\\\'") for word in keywordList]
		query = "SELECT * FROM Restaurant WHERE Restaurant_name LIKE '%" +str(keywordList[0]) + "%'"
		for x in range(len(keywordList)-1):
			query += " OR Restaurant_name LIKE '%" + str(keywordList[x+1]) + "%'"
		query += ";"
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
		cursor = conn.cursor()
		query = "SELECT * FROM Restaurant ORDER BY Restaurant_id DESC LIMIT 10;"
		cursor.execute(query)
		output = cursor.fetchall()
		cursor.close()
		conn.close()
		ret = list()
		for rest in output:
			ret.append(dict(ID=rest[0], Name=rest[1], Location_ID=rest[2], Category=rest[3], Cuisine=rest[4], Notes=rest[5], Image=rest[6]))

		return ret

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
		cursor = conn.cursor()
		query = "SELECT * FROM Orders WHERE User_ID = "+str(ID)+" ORDER BY Order_start_time DESC LIMIT 10;"
		cursor.execute(query)
		output = cursor.fetchall()
		cursor.close()
		conn.close()
		ret = list()
		for order in output:
			ret.append(dict(Order_ID=str(order[0]), User_ID=str(order[1]), Location_ID=str(order[2]), Order_start_time=str(order[3]), Order_end_time=str(order[4]), Order_status=str(order[5])))
		return ret

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
		cursor = conn.cursor()
		query = "SELECT * FROM Location WHERE Location_ID = "+str(ID)+";"
		cursor.execute(query)
		output = cursor.fetchall()
		cursor.close()
		conn.close()
		ret = list()
		for location in output:
			ret.append(dict(Location_ID=str(location[0]),Location_Street_1=str(location[1]), Location_Street_2=str(location[2]),Location_City=str(location[3]), Location_State=str(location[4]), Location_Zip=str(location[5]), Location_Longitude=str(location[6]), Location_Latitude=str(location[7]), API=str(location[8])))
		return ret

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
		cursor = conn.cursor()
		query = "SELECT * FROM Order_items WHERE Restaurant_ID = "+str(ID)+";"
		cursor.execute(query)
		output = cursor.fetchall()
		cursor.close()
		conn.close()
		ret = list()
		for order in output:
			ret.append(dict(Order_ID=order[0], Restaurant_ID=rest[1], Menu_ID=rest[2], Item_ID=rest[3], Item_Quantity=rest[4]))
		return ret


#get_restaurant_using_ID(7)
#get_restaurant_using_keyword('pizza')
#get_menu_items_using_restaurant_ID(9)
#print(get_recent_using_user_ID(1))
#print(get_favorites_using_user_ID(1))
