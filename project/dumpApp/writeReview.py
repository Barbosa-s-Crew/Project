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
		query = "INSERT INTO Reviews (Restaurant_ID, Order_ID, User_ID, Review_Rating, Review_Text "
		query += "VALUES(" + str(Restaurant_ID) + ", " + str(order_ID) + ", " + str(User_ID) + ", " + str(Review_Rating) + "\"" + str(Review_Text) + "\");"

		cursor.execute(query)
		cursor.commit()

		cursor.execute("SELECT MAX(Review_ID) AS Review_ID FROM Reviews")
		fetchedList = cursor.fetchall()
		print("ID from Reviews = " + fetchedList[0])

		cursor.close()
		conn.close()
		return fetchedList[0]['ReviewID']

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
		query = "SELECT * FROM Reviews WHERE User_ID=" + str(User_ID) + ";"
		cursor.execute(query)
		output = cursor.fetchall()
		print(output)
		return output
