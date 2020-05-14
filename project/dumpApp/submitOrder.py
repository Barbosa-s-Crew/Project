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


	def get_item_dictionary(self):
		item_dict = dict()
		item_dict['restaurant_ID'] = self.restaurant_ID
		item_dict['menu_ID'] = self.menu_ID
		item_dict['item_ID'] = self.item_ID
		item_dict['item_name'] = self.item_name
		item_dict['item_image'] = self.item_image
		item_dict['item_price'] = self.item_price
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
			cursor = conn.cursor(dictionary = True)
			query = "INSERT INTO Order_items (Order_ID, Restaurant_ID, Menu_ID, Item_ID, Item_Quantity)"
			query += " VALUES (\""+str(order_ID)+"\",\""+str(self.restaurant_ID)+"\", \""+str(self.menu_ID)+"\", \""+str(self.item_ID)+"\", \""+str(self.item_quantity)+"\");"
			cursor.execute(query)
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
		self.olist = []
		for item in dict_list:
			orderitem = order_item(item['restaurant_ID'],item['menu_ID'],item['item_ID'],item['item_name'],item['item_price'],item['item_quantity'],item['item_image'], )
			self.olist.append(orderitem)
		
	def convert_to_dict_list(self):
		dict_list = []
		if len(self.olist) > 0:
			for i in range(0,len(self.olist)):
				dict_list.append(self.olist[i].get_item_dictionary())
		return dict_list


	def add_order(self, order):
		self.olist.append(order)

	def add_item_by_ID(self, ID, quantity):
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
			cursor = conn.cursor(dictionary=True)
			query = "SELECT R.Restaurant_ID, M.Menu_ID, I.Item_ID, I.Item_name, I.Item_cost AS item_price, I.Item_image "
			query += "FROM Item I INNER JOIN Menu M ON I.Menu_ID=M.Menu_ID "
			query += "INNER JOIN Restaurant R ON M.Restaurant_ID=R.Restaurant_ID "
			query += "WHERE I.Item_ID = " + str(ID) + ";"
			cursor.execute(query)
			fetchedList = cursor.fetchall()
			query = "SELECT D.Item_ID, D.Deal_Price "
			query += "FROM Deal D "
			query += "WHERE D.Item_ID = " + str(fetchedList[0]['Item_ID']) +";"
			cursor.execute(query)
			fetchedList2=cursor.fetchall()

			if len(fetchedList2) > 0 :
				item = order_item(fetchedList[0]['Restaurant_ID'], fetchedList[0]['Menu_ID'], fetchedList[0]['Item_ID'], fetchedList[0]['Item_name'], fetchedList2[0]['Deal_Price'], quantity, fetchedList[0]['Item_image'])
			else:
				item = order_item(fetchedList[0]['Restaurant_ID'], fetchedList[0]['Menu_ID'], fetchedList[0]['Item_ID'], fetchedList[0]['Item_name'], fetchedList[0]['item_price'], quantity, fetchedList[0]['Item_image'])
			for i in range(0, len(self.olist)):
				if int(self.olist[i].item_ID) == item.item_ID:
					temp = int(self.olist[i].item_quantity)
					self.olist[i].item_quantity = str(temp + int(quantity))
					return
			

			conn.close()
			self.add_order(item)

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
			cursor = conn.cursor(dictionary=True)
			query = "INSERT INTO Orders (User_ID, Location_ID, Order_start_time, Order_Status) VALUES (\""+str(self.user_ID)+"\",\""+str(self.location_ID)+"\", CURTIME(),\""+str(self.status)+"\");"		
			cursor.execute(query)
			conn.commit()
			cursor.execute("SELECT max(Order_ID) AS Order_ID FROM Orders;")
			fetchedList = cursor.fetchall()
			print("ID from order: " + str(fetchedList[0]))
			cursor.close()
			conn.close()
			return fetchedList[0]['Order_ID']


	def change_order(self, added_item, quantity):
		for i in range(0, len(self.olist)):
			if self.olist[i].item_ID == added_item['item_ID']:
				if quantity <= 0:
					del self.olist[i]
				else:
					self.olist[i].item_quantity = quantity
				return
		temp_item = order_item(added_item['restaurant_ID'],added_item['menu_ID'],added_item['item_ID'],added_item['item_name'],added_item['item_price'], quantity, added_item['item_image'])
		self.add_order(temp_item)

	def get_order_subtotal(self):
		subtotal=0
		for item in self.olist:
			subtotal += float(item.item_price) * float(item.item_quantity)
		return float(subtotal)

	def get_order_total(self):
		return self.get_order_subtotal()*1.1

		
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
		cursor = conn.cursor(dictionary = True)
		query = "SELECT * FROM Orders WHERE Order_ID= \""+str(order_ID)+"\";"
		cursor.execute(query)
		fetched = cursor.fetchall()
		order = fetched[0]
		ret = order_list(order['User_ID'],order['Location_ID'],order['Order_status'])
		query = "SELECT * FROM Order_items WHERE Order_ID= \""+str(order_ID)+"\";"
		cursor.execute(query)
		fetched = cursor.fetchall()
		print(fetched)
		for order in fetched:
			print(order)
			ret.olist.append(order)
		return ret

def getOrderList(order_list_object_ID):
	try:
		print(order_list_object_ID)
		print(order_list.objects.get(id=order_list_object_ID))
		order_list_to_return = order_list.objects.get(id=order_list_object_ID)
		return order_list_to_return
	except (KeyError, order_list.DoesNotExist):
		order_list_to_return = None


def getOrderHistory(user_ID):
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
		cursor = conn.cursor(dictionary = True)
		query = "SELECT O.User_ID, OI.Item_Quantity, I.Item_name, I.Item_image, I.Item_cost, R.Restaurant_ID, I.Item_ID, M.Menu_ID "
		query += "FROM Orders O INNER JOIN Order_items OI ON O.Order_ID=OI.Order_ID "
		query += "INNER JOIN Item I ON I.Item_ID=OI.Item_ID "
		query += "INNER JOIN Menu M ON I.Menu_ID=M.Menu_ID "
		query += "INNER JOIN Restaurant R ON M.Restaurant_ID=R.Restaurant_id "
		query += "WHERE O.User_ID= " + str(user_ID) + " "
		query += "GROUP BY O.Order_ID "
		query += "LIMIT 5;"
		cursor.execute(query)
		fetched = cursor.fetchall()

		ret = order_list(user_ID,1,0)
		for order in fetched:
		 	print(order)
		 	ret.olist.append(order)
		print("*****************************fetched")
		print(fetched)
		print("*****************************fetched")
		return fetched

