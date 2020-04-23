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

	def __init__(self, restaurant_ID, menu_ID, item_ID, item_name, item_price, item_quantity
		, item_image):
		self.restaurant_ID = restaurant_ID
		self.menu_ID = menu_ID
		self.item_ID = item_ID
		self.item_name = item_name
		self.item_price = item_price
		self.item_quantity = item_quantity
		self.item_image = item_image


	def get_item_dictionary(self):
		item_dict = dict()
		item_dict['restaurant_ID'] = self.restaurant_ID
		item_dict['menu_ID'] = self.menu_ID
		item_dict['item_ID'] = self.item_ID
		item_dict['item_name'] = self.item_name
		item_dict['item_image'] = self.item_image
		item_dict['item_rice'] = self.item_price
		item_dict['item_quantity'] = self.item_quantity
		return item_dict


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
			cursor = conn.cursor(prepared = True)
			query = "INSERT INTO Order_items (Order_ID, Restaurant_ID, Menu_ID, Item_ID, Item_Quantity) VALUES (?, ?, ?, ?, ?);"
			query_tuple = (order_ID, self.restaurant_ID, self.menu_ID, self.item_ID, self.item_quantity)
			cursor.execute(query, query_tuple)
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
				dict_list.append(olist[i].get_item_dictionary)
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
		olist = list()

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
			cursor = conn.cursor(prepared = True)
			query = "INSERT INTO Orders (User_ID, Location_ID, Order_start_time, Order_Status) VALUES (?, ?, CURTIME(), ?);"
			query_tuple = (self.user_ID, self.location_ID, self.status)
			cursor.execute(query, query_tuple)
			conn.commit()
			cursor.execute("SELECT max(Order_ID) FROM Orders;")
			order_ID = cursor.fetchall()
			print("ID from sorder: " + str(order_ID))
			conn.close()
			return order_ID[0][0]


	def change_order(added_item, quantity):
		for i in range(0, len(self.olist)):
			if self.olist[i].item_ID == added_item['ID']:
				if quantity <= 0:
					del self.olist[i]
				else:
					self.olist[i].quantity = quantity
				return
		temp_item = order_item(added_item['restaurant_ID'],added_item['menu_ID'],added_item['item_ID'],added_item['item_name'],added_item['item_price'],added_item['item_quantity'],added_item['item_image'])
		self.add_order(temp_item)
		
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
		cursor = conn.cursor(prepared = True)
		query = "SELECT * FROM Orders WHERE Order_ID= ?"
		query_tuple = (order_ID,)
		cursor.execute(query, query_tuple)
		fetched = cursor.fetchall()
		order = fetch[0]
		#Full string from the query:Order_ID=str(order[0]),User_ID=str(order[1]),Location_ID=str(order[2]),Order_start_time=str(order[3]),Order_end_time=str(order[4]),Order_status=str(order[5])
		ret = order_list(order[1],order[2],order[5])
		query = "SELECT * FROM Order_items WHERE Order_ID= ?"
		query_tuple = (order_ID,)
		cursor.execute(query, query_tuple)
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



