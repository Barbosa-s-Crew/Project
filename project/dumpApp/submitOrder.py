import mysql.connector
from mysql.connector import errorcode
from . import DBSetup

def submitItem(that_dict):
	# Obtain connection string information from the portal
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
		cursor = conn.cursor()
		cursor.execute("INSERT INTO Order_items (Order_ID, Restaurant_ID, Menu_ID, Item_ID, Item_Quantity) VALUES ('"+that_dict.get("Order_ID")+"', '"+that_dict.get("Restaurant_ID")+"', '"+that_dict.get("Menu_ID")+"', '"+that_dict.get("Item_ID")+"', '"+that_dict.get("Item_Quantity")+"');")
		conn.commit()
		conn.close()




def submitOrder(that_dict):
	# Obtain connection string information from the portal
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
		cursor = conn.cursor()
		cursor.execute("INSERT INTO Orders (Order_ID, User_ID, Location_ID, Order_start_time, Order_Status) VALUES ('"+that_dict.get("Order_ID")+"', '"+that_dict.get("User_ID")+"', '"+that_dict.get("Location_ID")+"', '"+that_dict.get("Order_start_time")+"', '"+that_dict.get("Order_status")+"');")
		conn.commit()
		conn.close()


