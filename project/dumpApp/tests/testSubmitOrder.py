from django.test import SimpleTestCase
from . import DBSetup
from dumpApp import submitOrder
import mysql.connector
from mysql.connector import errorcode

class submitOrderTestCase(SimpleTestCase):
	#def submit_test():
	#def getOrder_test(order_ID):
	def test_submit_order_functions(self):
		orderHistory = submitOrder.getOrderHistory(1)
		self.assertEqual(orderHistory[0],{'User_ID': 1, 'Item_Quantity': 3, 'Item_name': 'Item 6', 'Item_image': None, 'Item_cost': 25.0, 'Restaurant_ID': 3, 'Item_ID': 1, 'Menu_ID': 4})

		testOrder =  submitOrder.order_list(1,1,0)
		testOrder.create_from_dict_list([dict(restaurant_ID=3,menu_ID=4,item_ID=1,item_name='Item 6',item_price=25.0,item_quantity=3,item_image=None,),])
		testOrder.add_item_by_ID(15,1)
		orderDict = testOrder.convert_to_dict_list()
		self.assertEqual(orderDict,[{'restaurant_ID': 3, 'menu_ID': 4, 'item_ID': 1, 'item_name': 'Item 6', 'item_image': None, 'item_price': 25.0, 'item_quantity': 3}, {'restaurant_ID': 7, 'menu_ID': 7, 'item_ID': 15, 'item_name': 'Fried Shrimp', 'item_image': 'https://spicysouthernkitchen.com/wp-content/uploads/Fried-Shrimp-4.jpg', 'item_price': 11.0, 'item_quantity': 1}])
		
		testOrder.change_order(dict(restaurant_ID=3,menu_ID=4,item_ID=1,item_name='Item 6',item_price=25.0,item_quantity=3,item_image=None,), 5)
		orderDict = testOrder.convert_to_dict_list()
		self.assertEqual(orderDict,[{'restaurant_ID': 3, 'menu_ID': 4, 'item_ID': 1, 'item_name': 'Item 6', 'item_image': None, 'item_price': 25.0, 'item_quantity': 5}, {'restaurant_ID': 7, 'menu_ID': 7, 'item_ID': 15, 'item_name': 'Fried Shrimp', 'item_image': 'https://spicysouthernkitchen.com/wp-content/uploads/Fried-Shrimp-4.jpg', 'item_price': 11.0, 'item_quantity': 1}])
		testOrder.add_order(submitOrder.order_item(7,9,27,"Green Bean Shrimp with Oyster Sauce",13.5,1,"https://previews.123rf.com/images/boyisteady/boyisteady1612/boyisteady161200001/69709404-mixed-vegetables-and-shrimps-with-oyster-sauce-serve-on-dish-.jpg"))
		orderDict = testOrder.convert_to_dict_list()
		print("Third Assert")
		self.assertEqual(orderDict,[{'restaurant_ID': 3, 'menu_ID': 4, 'item_ID': 1, 'item_name': 'Item 6', 'item_image': None, 'item_price': 25.0, 'item_quantity': 5}, {'restaurant_ID': 7, 'menu_ID': 7, 'item_ID': 15, 'item_name': 'Fried Shrimp', 'item_image': 'https://spicysouthernkitchen.com/wp-content/uploads/Fried-Shrimp-4.jpg', 'item_price': 11.0, 'item_quantity': 1}, {'restaurant_ID': 7, 'menu_ID': 9, 'item_ID': 27, 'item_name': 'Green Bean Shrimp with Oyster Sauce', 'item_image': 'https://previews.123rf.com/images/boyisteady/boyisteady1612/boyisteady161200001/69709404-mixed-vegetables-and-shrimps-with-oyster-sauce-serve-on-dish-.jpg', 'item_price': 13.5, 'item_quantity': 1}])
		orderTotal = testOrder.get_order_subtotal()
		self.assertEqual(orderTotal,149.5)
		testOrder.submit()

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
			cursor.execute("SELECT max(Order_ID) AS Order_ID FROM Orders;")
			fetchedList = cursor.fetchall()
			cursor.close()
			conn.close()
			self.assertNotEqual(submitOrder.getOrder(fetchedList[0]['Order_ID']),[])