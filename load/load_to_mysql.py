import sys
from pathlib import Path

from pyspark.sql import SparkSession

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str("BASE_DIR"))

from config import MYSQL_CONFIG

def load_to_mysql():
    spark = (
        SparkSession.builder
        .appName("LoadUserBehaviorToMySQL")
        .master("loacl[4]")
        .config("spark.dirver.memoery","4g")
        .config("spark.jar.packages","com.mysql:mysql_connection-j:8.4.0")
        .getOrCreate()
    )

    input_path = "data/cleaned/user_behavior_cleaned.parquet"

    jdbc_url = (
        f"jdbc:mysql://{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/"
        f"{MYSQL_CONFIG['database']}?useSSL=false&serverTimezone=Asia/Shanghai"
    )

    df = spark.read.parquet(input_path)

    sample_df = df.limit(10000)

    (sample_df.write
        .format("jdbc") 
        .option("url",jdbc_url)
        .option("dbtable","user_behavior")
        .option("user",MYSQL_CONFIG["user"])
        .option("password",MYSQL_CONFIG["password"])
        .option("driver","com.mysql.cj.jdbc.Driver")
        .mode("append")
        .save()
    )

    print("loaded 10000 row to user_behavior")

    spark.stop()

if __name__ =="__main__":
    load_to_mysql()