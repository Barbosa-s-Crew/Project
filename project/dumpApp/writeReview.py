import mysql.connector
from mysql.connector import errorcode
from . import DBSetup


def writeReview(Restaurant_ID, Order_ID, User_ID, Review_Rating, Review_Text):
	config = DBSetup.setup_config()

	try:
		conn = mysql.connector.connect(**config)
		print("Connection established")
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with the user name or password")
		elif err.errno == errorcode.ER.BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)

	else:
		cursor = conn.cursor(dictionary = True)
		query = "INSERT INTO Reviews (Restaurant_ID, Order_ID, User_ID, Review_Rating, Review_Text) "
		query += "VALUES(" + str(Restaurant_ID) + ", " + str(Order_ID) + ", " + str(User_ID) + ", " + str(Review_Rating) + ",\'" + str(Review_Text) + "\');"

		cursor.execute(query)
		conn.commit()

		cursor.execute("SELECT MAX(Review_ID) AS Review_ID FROM Reviews")
		fetchedList = cursor.fetchall()
		print("ID from Reviews = " + str(fetchedList[0]['Review_ID']))

		cursor.close()
		conn.close()
		return fetchedList[0]['Review_ID']

def getReview(User_ID):
	config = DBSetup.setup_config()

	try:
		conn = mysql.connector.connect(**config)
		print("Connection established")
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with the user name or password")
		elif err.errno == errorcode.ER.BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cursor = conn.cursor(dictionary = True)
		#query = "SELECT * FROM Reviews WHERE User_ID=" + str(User_ID) + ";"

		query = "SELECT Rv.Review_ID, Rv.Review_Rating, Rv.Review_Text, Rs.Restaurant_Name "
		query += "FROM Reviews Rv INNER JOIN Restaurant Rs ON Rv.Restaurant_ID = Rs.Restaurant_id "
		query += "WHERE Rv.User_ID=" + str(User_ID) + " "
		query += "ORDER BY Rv.Review_ID DESC "
		query += "LIMIT 4";

		cursor.execute(query)
		output = cursor.fetchall()
		print(output)
		return output

def get_reviews_by_restaurant_ID(Restaurant_ID):
	config = DBSetup.setup_config()

	try:
		conn = mysql.connector.connect(**config)
		print("Connection established")
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with the user name or password")
		elif err.errno == errorcode.ER.BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cursor = conn.cursor(dictionary = True)
		#query = "SELECT * FROM Reviews WHERE User_ID=" + str(User_ID) + ";"

		query = "SELECT Rv.Review_ID, Rv.Review_Rating, Rv.Review_Text, Rs.Restaurant_Name "
		query += "FROM Reviews Rv INNER JOIN Restaurant Rs ON Rv.Restaurant_ID = Rs.Restaurant_id "
		query += "WHERE Rv.Restaurant_ID = " + str(Restaurant_ID) + " "
		query += "ORDER BY Rv.Review_ID "
		query += "LIMIT 5;"

		cursor.execute(query)
		output = cursor.fetchall()
		print(output)
		return output
