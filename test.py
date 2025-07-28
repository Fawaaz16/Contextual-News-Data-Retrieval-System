import pymysql

try:
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="Iamsorry1"
    )
    print("Connected successfully!")
    connection.close()
except pymysql.Error as err:
    print(f"Error: {err}")