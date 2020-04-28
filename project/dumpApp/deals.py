import time
import mysql.connector
from mysql.connector import errorcode
from . import DBSetup

deals = list()
time_count = time.perf_counter()
UPDATE_RATE = 10 * 60 # in seconds

def get_deals():
	global deals
	elapsed_time = time.perf_counter() - time_count
	if not deals or elapsed_time > UPDATE_RATE:
		output = ""
		# Obtain connection string information from the portal
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
			query =  "SELECT D.Deal_Price, I.Item_name, I.item_image, R.Restaurant_Name, I.Menu_ID, I.Item_ID, R.Restaurant_id "
			query += "FROM Deal D  INNER JOIN Item I ON D.Item_ID=I.Item_ID "
			query += "INNER JOIN Menu M ON I.Menu_ID=M.Menu_ID "
			query += "INNER JOIN Restaurant R ON M.Restaurant_ID=R.Restaurant_ID "
			query += "WHERE D.Deal_Start_Time < CURDATE() AND D.Deal_End_Time > CURDATE(); "
			cursor.execute(query)
			fetched_deals = cursor.fetchall()
			cursor.close()
			conn.close()
			deals = format_deals(fetched_deals)

	return deals

def format_deals(tup):
	list_of_deals = list()
	for d in tup:
		print(d)
		list_of_deals.append(dict(Price=d[0], Name=d[1], Image=d[2], Restaurant_Name=d[3], Menu_ID=d[4], Item_ID=d[5], Restaurant_ID=d[6]))
	return list_of_deals
