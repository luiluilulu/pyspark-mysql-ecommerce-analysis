from utils.spark_utils import create_spark
from utils.path_utils import CLEANED_DATA_PATH

def  check_cleaned_data():

    spark = create_spark("CheckCleanedUserBehavior")

    df = spark.read.parquet(str(CLEANED_DATA_PATH))
    
    df.show(5)

    df.printSchema()

    df.groupBy("behavior_type").count().show()

    df.selectExpr(
        "min(behavior_date) as min_date",
        "max(behavior_date) as max_date"
    ).show()

    spark.stop()

if __name__ == "__main__":
    check_cleaned_data()