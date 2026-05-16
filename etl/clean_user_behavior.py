from pyspark.sql import SparkSession
from pyspark.sql.functions import col,from_unixtime,to_date,hour
from pyspark.sql.types import StructType,StructField,LongType,StringType
from utils.path_utils import RAW_DATA_PATH, CLEANED_DATA_PATH
from utils.spark_utils import create_spark

def clean_user_behavior():
    spark = create_spark("CleanUserBehavior")
    schema = StructType([
            StructField("user_id",LongType(),True),
            StructField("item_id",LongType(),True),
            StructField("category_id",LongType(),True),
            StructField("behavior_type",StringType(),True),
            StructField("timestamp",LongType(),True),
        ])
    
    df = spark.read.csv(str(RAW_DATA_PATH),header=False,schema=schema)

    cleaned_df = (
        df 
        .dropna(subset=["user_id","item_id","category_id","behavior_type","timestamp"])
        .filter(col("behavior_type").isin("pv","fav","cart","buy"))
        .withColumn("behavior_time",from_unixtime(col("timestamp")))
        .withColumn("behavior_date",to_date(col("behavior_time")))
        .withColumn("behavior_hour",hour(col("behavior_time")))
        .filter(
            (col("behavior_date") >="2017-11-25") &
            (col("behavior_date")<="2017-12-03")
        )
        .select(
            "user_id",
            "item_id",
            "category_id",
            "behavior_type",
            "behavior_time",
            "behavior_date",
            "behavior_hour"
        )
    )

    cleaned_df.coalesce(4).write.mode("overwrite").parquet(str(CLEANED_DATA_PATH))

    print("cleaned data saved to:",CLEANED_DATA_PATH)

    spark.stop( )


if __name__ == "__main__":
    clean_user_behavior()