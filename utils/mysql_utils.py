import pymysql
from utils.config_utils import MYSQL_CONFIG

def get_mysql_connection():
    #link to MySQL
    return pymysql.connect(**MYSQL_CONFIG)

def truncate_table(table_name):
    #Only allow Known table name
    allowed_tables = {"user_behavior"}

    if table_name not in allowed_tables:
        raise ValueError(f"Table is not allowed: {table_name}")
    conn =get_mysql_connection()

    cursor = conn.cursor()

    cursor.execute(f"TRUNCATE TABLE {table_name};")
    conn.commit()

    cursor.close()
    conn.close()