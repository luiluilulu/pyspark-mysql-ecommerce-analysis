import pymysql 
from config import MYSQL_CONFIG
def test_connection():
    conn = pymysql.connect(**MYSQL_CONFIG)

    cursor = conn.cursor()

    cursor.execute("SELECT DATABASE();")

    result = cursor.fetchone()

    print("当前连接的数据库:",result[0])

    cursor.close()
    conn.close()

if __name__  == "__main__":
    test_connection()