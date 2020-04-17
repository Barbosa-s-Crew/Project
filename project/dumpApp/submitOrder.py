import mysql.connector
from mysql.connector import errorcode
from . import DBSetup

class order_item:
	restaurant_ID = ''
	menu_ID = ''
	item_ID = ''
	item_name = ''
	item_price = 0
	item_quantity = 0
	item_image = ''

	def __init__(self, restaurant_ID, menu_ID, item_ID, item_name, item_price, item_quantity, item_image):
		self.restaurant_ID = restaurant_ID
		self.menu_ID = menu_ID
		self.item_ID = item_ID
		self.item_name = item_name
		self.item_price = item_price
		self.item_quantity = item_quantity
		self.item_image = item_image

	def submitItem(self, order_ID):
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
			cursor.execute("INSERT INTO Order_items (Order_ID, Restaurant_ID, Menu_ID, Item_ID, Item_Quantity) VALUES ('"+str(order_ID)+"', '"+str(self.restaurant_ID)+"', '"+str(self.menu_ID)+"', '"+str(self.item_ID)+"', '"+str(self.item_quantity)+"');")
			conn.commit()
			conn.close()


#----------------------------------------------------------------------
class order_list:
	olist = []
	user_ID = ''
	location_ID = ''
	status = ''

	#this will init the orders class with an empty list
	def __init__(self, user_ID, location_ID, status):
		self.user_ID = user_ID
		self.location_ID = location_ID
		self.status = status
	def create_from_dict_list(self, dict_list):
		for item in dict_list:
			orderitem = order_item(item['restaurant_ID'],item['menu_ID'],item['item_ID'],item['item_name'],item['item_price'],item['item_quantity'],item['item_image'])
			self.olist.append(orderitem)
		
	def convert_to_dict_list(self):
		dict_list = []
		print(" IN convert_to_dict_list")
		if len(self.olist) > 0:
			for i in range(0,len(self.olist)):
				item_dict = dict()
				item_dict['Name'] = self.olist[i].item_name
				item_dict['Image'] = self.olist[i].item_image
				item_dict['Price'] = self.olist[i].item_price
				item_dict['Quantity'] = self.olist[i].item_quantity

				dict_list.append(item_dict)
		print(dict_list)
		return dict_list


	def add_order(self, order):
		self.olist.append(order)
		print(self.olist)

	def submit(self):
		ID = self.submitOrder()
		print("ID is: " + str(ID))
		for i in range(0, len(self.olist)):
			self.olist[i].submitItem(ID)

	def submitOrder(self):
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
			cursor.execute("INSERT INTO Orders (User_ID, Location_ID, Order_start_time, Order_Status) VALUES ('"+str(self.user_ID)+"', '"+str(self.location_ID)+"', CURTIME(), '"+str(self.status)+"');")
			conn.commit()
			cursor.execute("SELECT max(Order_ID) FROM Orders;")
			order_ID = cursor.fetchall()
			print("ID from sorder: " + str(order_ID))
			conn.close()
			return order_ID[0][0]

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
		#Full string from the query:Order_ID=str(order[0]),User_ID=str(order[1]),Location_ID=str(order[2]),Order_start_time=str(order[3]),Order_end_time=str(order[4]),Order_status=str(order[5])
		ret = order_list(order[1],order[2],order[5])
		cursor.execute("SELECT * FROM Order_items WHERE Order_ID='"+str(order_ID)+"'")
		fetched = cursor.fetchall()
		for order in fetched:
			ret.olist.append(dict(Order_ID=str(order[0]), Restaurant_ID=str(order[1]), Menu_ID=str(order[2]), Item_ID=str(order[3]), Item_Quantity=str(order[4])))
		return ret

def getOrderList(order_list_object_ID):
	try:
		print(order_list_object_ID)
		print(order_list.objects.get(id=order_list_object_ID))
		order_list_to_return = order_list.objects.get(id=order_list_object_ID)
		return order_list_to_return
	except (KeyError, order_list.DoesNotExist):
		order_list_to_return = None
