from pyspark.sql import SparkSession

from utils.path_utils import MYSQL_JAR_PATH


def create_spark(app_name, with_mysql=False):
    #Create local Sparksession
    builder = (
        SparkSession.builder
        .appName(app_name)
        .master("local[4]")
        .config("spark.driver.memory","4g")
        .config("spark.sql.shuffle.partitions","4")
    )
    if with_mysql:
         builder = builder.config("spark.jars", str(MYSQL_JAR_PATH))
    return builder.getOrCreate()