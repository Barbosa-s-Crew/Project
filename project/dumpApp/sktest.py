import mysql.connector
from mysql.connector import errorcode
from . import DBSetup

def getDB():
  output = ""
  # Obtain connection string information from the portal
  config = DBSetup.setup_config()

  # Construct connection string
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
      #conn.commit()
      cursor.execute("SHOW TABLES")
      tables = cursor.fetchall()
      for table in tables:
          #print("TABLE_NAME:"+table[0])
          output += ("TABLE_NAME:"+table[0]+'\n')
          cursor.execute("DESCRIBE "+table[0])
          descriptions = cursor.fetchall()
          for description in descriptions:
              #print('{:20}'.format(description[0]),end="")
              output += ('{:20}'.format(description[0]))
          #print("")
          output += '\n'
          cursor.execute("SELECT * FROM "+table[0])
          rows = cursor.fetchall()
          for row in rows:
              for element in row:
                  #print('{:20}'.format(str(element)),end="")
                  output += ('{:20}'.format(str(element)))
              #print("")
              output += '\n'

      cursor.close()
      conn.close()
      return output

getDB()
