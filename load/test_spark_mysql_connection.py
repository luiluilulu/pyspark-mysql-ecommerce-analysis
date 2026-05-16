from utils.config_utils import MYSQL_CONFIG
from utils.spark_utils import create_spark

def test_spark_mysql_connection():
    spark = create_spark("TestSparkMySQLConnection",with_mysql=True)
    jdbc_url=(
        f"jdbc:mysql://{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/"
        f"{MYSQL_CONFIG['database']}?useSSL=false&serverTimezone=Asia/Shanghai"
    )

    df = (
        spark.read
        .format("jdbc")
        .option("url",jdbc_url)
        .option("dbtable","user_behavior")
        .option("user",MYSQL_CONFIG["user"])
        .option("password",MYSQL_CONFIG["password"])
        .option("driver","com.mysql.cj.jdbc.Driver")
        .load()
    )

    df.printSchema()

    print("user_behavior current row count:",df.count())

    spark.stop()

if __name__ =="__main__":
    test_spark_mysql_connection()