from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType,StructField,LongType,StringType
from utils.path_utils import RAW_DATA_PATH
from utils.spark_utils import create_spark

def check_raw_data():

    spark = create_spark("CheckRawUserBehavior")

    schema = StructType([
        StructField("user_id",LongType(),True),
        StructField("item_id",LongType(),True),
        StructField("category_id",LongType(),True),
        StructField("behavior_type",StringType(),True),
        StructField("timestamp",LongType(),True),
    ])
    df =  spark.read.csv(str(RAW_DATA_PATH),header=False,schema=schema)

    df.show(5)

    df.printSchema()

    spark.stop()

if __name__ == "__main__":
    check_raw_data()