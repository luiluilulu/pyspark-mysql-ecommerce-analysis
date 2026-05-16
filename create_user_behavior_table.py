from utils.mysql_utils import get_mysql_connection

def create_user_behavior_table():
    conn =get_mysql_connection()
    cursor = conn.cursor()

    create_sql = """
    CREATE TABLE IF NOT EXISTS user_behavior(
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        user_id BIGINT NOT NULL,
        item_id BIGINT NOT NULL,
        category_id BIGINT NOT NULL,
        behavior_type VARCHAR(20) NOT NULL,
        behavior_time DATETIME NOT NULL,
        behavior_date DATE NOT NULL,
        behavior_hour INT NOT NULL
    );
    """

    cursor.execute(create_sql)

    conn.commit()

    print("user_behavior table created successfully")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_user_behavior_table()