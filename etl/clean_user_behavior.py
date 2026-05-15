from pyspark.sql import SparkSession
from pyspark.sql.functions import col,from_unixtime,to_date,hour
from pyspark.sql.types import StructType,StructField,LongType,StringType

def clean_user_behavior():
    spark = (SparkSession.builder
                .appName("CheckRawUserBehavior")
                .master("local[*]")
                .config("spark.driver.memory","4g")
                .config("spark.sql.shuffle.partitions","4")
                .getOrCreate()
        )

    input_path = "data/UserBehavior.csv"
    output_path ="data/cleaned/user_behavior_cleaned.parquet"
    schema = StructType([
            StructField("user_id",LongType(),True),
            StructField("item_id",LongType(),True),
            StructField("category_id",LongType(),True),
            StructField("behavior_type",StringType(),True),
            StructField("timestamp",LongType(),True),
        ])
    
    df = spark.read.csv(input_path,header=False,schema=schema)

    cleaned_df = (
        df 
        .dropna(subset=["user_id","item_id","category_id","behavior_type","timestamp"])
        .filter(col("behavior_type").isin("pv","fav","cart","buy"))
        .withColumn("behavior_time",from_unixtime(col("timestamp")))
        .withColumn("behavior_date",to_date(col("behavior_time")))
        .withColumn("behavior_hour",hour(col("behavior_time")))
        .filter(
            (col("behavior_date") >="2017-11-05") &
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

    cleaned_df.coalesce(4).write.mode("overwrite").parquet(output_path)

    print("claened data saved to:",output_path)

    spark.stop( )


if __name__ == "__main__":
    clean_user_behavior()