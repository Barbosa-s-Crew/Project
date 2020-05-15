import mysql.connector
from mysql.connector import errorcode
from . import DBSetup


def update_profile(User_ID, email, username, phone):
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
		query = "UPDATE Users AS U "
		query += "SET U.User_Email=\"" + str(email) + "\", U.User_Cell=\"" + str(phone) + "\", U.User_name=\"" + str(username) + "\" "
		query += "WHERE U.User_ID=" + str(User_ID) + ";"

		cursor.execute(query)
		conn.commit()

		cursor.close()
		conn.close()