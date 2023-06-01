import mysql.connector
from mysql.connector import errorcode

def inputData(query):
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "root",
            database = "soh"
        )
        ptr = mydb.cursor(buffered=True)
        a = ptr.execute(query)
        mydb.commit()
        mydb.close()
        print("query success")
        return a
    except mysql.connector.Error as err:
        print(err.errno)
        return err

def getData(query):
    try :
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "root",
            database = "soh"
        )
        ptr = mydb.cursor(buffered=True)
        ptr.execute(query)
        count = ptr.rowcount
        return count
    except mysql.connector.Error as err :
        return err

def getDataValue(query):
    try :
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "root",
            database = "soh"
        )
        ptr = mydb.cursor(buffered=True)
        ptr.execute(query)
        return ptr
    except mysql.connector.Error as err :
        return err

def getCursor():
    try :
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "root",
            database = "soh"
        )
        ptr = mydb.cursor(buffered=True)
        print(ptr)
        return ptr
    except mysql.connector.Error as err :
        return err