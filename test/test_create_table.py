import pymysql
from config import MYSQL_CONFIG

def create_test_table():
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    
    create_sql = """
    CREATE TABLE IF NOT EXISTS test_user(
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50),
        age INT
    );
"""
    cursor.execute(create_sql)

    conn.commit()

    print("测试表 test_user 创建成功")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_test_table()