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
		cursor.execute("INSERT INTO Order_items (Order_ID, Restaurant_ID, Menu_ID, Item_ID, Item_Quantity) VALUES ('"+str(that_dict.get("Order_ID"))+"', '"+str(that_dict.get("Restaurant_ID"))+"', '"+str(that_dict.get("Menu_ID"))+"', '"+str(that_dict.get("Item_ID"))+"', '"+str(that_dict.get("Item_Quantity"))+"');")
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
		cursor.execute("INSERT INTO Orders (Order_ID, User_ID, Location_ID, Order_start_time, Order_Status) VALUES ('"+str(that_dict.get("Order_ID"))+"', '"+str(that_dict.get("User_ID"))+"', '"+str(that_dict.get("Location_ID"))+"', '"+str(that_dict.get("Order_start_time"))+"', '"+str(that_dict.get("Order_status"))+"');")
		conn.commit()
		conn.close()


def getOrder(order_ID):
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
		cursor.execute("SELECT * FROM Orders WHERE Order_ID='"+str(order_ID)+"'")
		fetched = cursor.fetchall()
		order = fetch[0]
		ret = list()
		ret.append(dict(Order_ID=str(order[0]),User_ID=str(order[1]),Location_ID=str(order[2]),Order_start_time=str(order[3]),Order_end_time=str(order[4]),Order_status=str(order[5])))
		cursor.execute("SELECT * FROM Order_items WHERE Order_ID='"+str(order_ID)+"'")
		fetched = cursor.fetchall()
		for order in fetched:
			ret.append(dict(Order_ID=str(order[0]), Restaurant_ID=str(order[1]), Menu_ID=str(order[2]), Item_ID=str(order[3]), Item_Quantity=str(order[4])))
		return ret
