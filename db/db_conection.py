import pymysql

def get_connection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='example',
                                 db='mydb',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection