from utils.config_utils import MYSQL_CONFIG
from utils.path_utils import CLEANED_DATA_PATH
from utils.spark_utils import create_spark
from utils.mysql_utils import truncate_table

def load_to_mysql():
    spark =create_spark("LoadUserBehaviorToMySQL",with_mysql=True)
    
    jdbc_url = (
        f"jdbc:mysql://{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/"
        f"{MYSQL_CONFIG['database']}?useSSL=false&serverTimezone=Asia/Shanghai"
    )

    df = spark.read.parquet(str(CLEANED_DATA_PATH))

    sample_df = df.limit(10000)

    CLEAR_BEFORE_LOAD = True

    if CLEAR_BEFORE_LOAD:
        truncate_table("user_behavior")

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