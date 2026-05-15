from pyspark.sql import SparkSession


def  check_cleaned_builder():

    spark = (
        SparkSession.builder
        .appName("CheckCleanedUserBehavior")
        .master("local[4]")
        .config("spark.driver.memory","4g")
        .getOrCreate()
    )

    input_path = "data/cleaned/user_behavior_cleaned.parquet"

    df = spark.read.parquet(input_path)
    
    df.show(5)

    df.printSchema()

    df.groupBy("behavior_type").count().show()

    df.selectExpr(
        "min(behavior_date) as min_date",
        "max(behavior_date) as max_date"
    ).show()

    spark.stop()

if __name__ == "__main__":
    check_cleaned_builder()