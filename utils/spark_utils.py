from pyspark.sql import SparkSession

from utils.path_utils import MYSQL_JAR_PATH
from utils.config_utils import get_jdbc_url,MYSQL_CONFIG

def create_spark(app_name, with_mysql=False):
    #Create local Sparksession
    builder = (
        SparkSession.builder
        .appName(app_name)
        .master("local[4]")
        .config("spark.driver.memory","4g")
        .config("spark.sql.shuffle.partitions","4")
        .config("spark.driver.bindAddress","127.0.0.1")
        .config("spark.driver.host", "127.0.0.1")
    )
    if with_mysql:
         builder = builder.config("spark.jars", str(MYSQL_JAR_PATH))
    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark

def write_df_to_mysql(df,table_name,mode="overwrite"):
     (
    df.write
    .format("jdbc")\
    .option("url",get_jdbc_url())
    .option("dbtable",table_name)
    .option("user",MYSQL_CONFIG["user"])
    .option("password",MYSQL_CONFIG["password"])
    .option("driver","com.mysql.cj.jdbc.Driver")
    .mode(mode)
    .save()
)