import pymysql
from config import MYSQL_CONFIG

def insert_and_query():
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    insert_sql = """
    INSERT INTO test_user (name,age)
    VALUES (%s,%s);
    """
    cursor.execute(insert_sql,("Alice",20))

    conn.commit()

    select_sql ="""
    SELECT id,name,age FROM test_user;
    """
    cursor.execute(select_sql)

    rows =cursor.fetchall()
    for row in rows:
        print(row)

    cursor.execute("SELECT id ,name , age FROM test_user WHERE age >= %s;",(20,))
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    insert_and_query()