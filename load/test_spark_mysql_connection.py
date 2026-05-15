from pyspark.sql import SparkSession
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
from config  import MYSQL_CONFIG

def test_spark_mysql_connection():
    spark = (
        SparkSession.builder
        .appName("TestSparkMySQLConnection")
        .master("local[4]")
        .config("spark.driver.memory","4g")
        .config("spark.jars.packages","com.mysql:mysql-connector-j:8.4.0")
        .getOrCreate()
    )
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

    print("user_behavior 当前行数:",df.count())

    spark.stop()

if __name__ =="__main__":
    test_spark_mysql_connection()