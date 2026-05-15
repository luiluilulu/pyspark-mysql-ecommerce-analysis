from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType,StructField,LongType,StringType

def check_raw_data():

    spark = (SparkSession.builder
             .appName("CheckRawUserBehavior")
             .master("local[*]")
             .getOrCreate()
    )
    
    file_path = "data/UserBehavior.csv"

    schema = StructType([
        StructField("user_id",LongType(),True),
        StructField("item_id",LongType(),True),
        StructField("category_id",LongType(),True),
        StructField("behavior_type",StringType(),True),
        StructField("timestamp",LongType(),True),
    ])
    df =  spark.read.csv(file_path,header=False,schema=schema)

    df.show(5)

    df.printSchema()

    spark.stop()

if __name__ == "__main__":
    check_raw_data()