import mysql.connector
from mysql.connector import errorcode
from . import DBSetup


config = DBSetup.setup_config()
def getLocationID(that_dict):
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
		query = "SELECT * FROM Location WHERE Location_Street_1=?, Location_Street_2=?, Location_City=?, Location_State=?, Location_Zip=?"
		query_tuple = (that_dict.get("Street1"),that_dict.get("Street2"),that_dict.get("City"),that_dict.get("State"),that_dict.get("Zip"))
		cursor.execute(query, query_tuple)
		tupleC = cursor.fetchall()
		if len(tupleC)==0:
			print("Location not found!")
		else:
			print("Location Found!")
			return getLocationDict(tupleC[0])


def getLocation(locationID):
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
		query = "SELECT * FROM Location WHERE Location_ID=?"
		query_tuple = (locationID,)
		cursor.execute(query, query_tuple)
		tupleC = cursor.fetchall()
		if len(tupleC)==0:
			print("Location not found!")
		else:
			print("Location Found!")
			return getLocationDict(tupleC[0])

def getLocationDict(tup):
	this_dict = dict(ID=tup[0],Street1=tup[1],Street2=tup[2],City=tup[3],State=tup[4],Zip=tup[5],Long=tup[6],Lat=tup[7],API=tup[8])
	return this_dict

def getPaymentID(that_dict):
	a =0


