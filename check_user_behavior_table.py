from utils.mysql_utils import get_mysql_connection


def check_table():
    # 连接 MySQL
    conn = get_mysql_connection()
    cursor = conn.cursor()

    # 查看 user_behavior 表结构
    cursor.execute("DESC user_behavior;")

    # 取出所有字段信息
    rows = cursor.fetchall()

    # 打印字段结构
    for row in rows:
        print(row)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    check_table()
