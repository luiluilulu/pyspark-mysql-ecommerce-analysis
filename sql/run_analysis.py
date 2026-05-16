from utils.path_utils import ANALYSIS_SQL_PATH
from utils.mysql_utils import get_mysql_connection

def run_analysis():

    sql_text = ANALYSIS_SQL_PATH.read_text(encoding="utf-8")
    #Read all SQL satements
    sql_list = [
        sql.strip()
        for sql in sql_text.split(";")
        if sql.strip()
    ]
    #Connect MySQL
    conn =get_mysql_connection()
    cursor = conn.cursor()
    #Execut each SQL statement
    for index , sql in enumerate(sql_list,start=1):
        print(f"\n-- Query {index}")
        print(sql)

        cursor.execute(sql)

        rows = cursor.fetchall()

        for row in rows:
            print(row)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    run_analysis()