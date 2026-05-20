from utils.spark_utils import create_spark
from utils.path_utils import CLEANED_DATA_PATH

spark = create_spark("QualityCheck")
df = spark.read.parquet(str(CLEANED_DATA_PATH))
df.createOrReplaceTempView("user_behavior")

result = spark.sql("""
    SELECT
        COUNT(*)                AS total_rows,
        COUNT(DISTINCT user_id) AS user_cnt,
        MIN(behavior_date)      AS min_date,
        MAX(behavior_date)      AS max_date,
        SUM(CASE WHEN user_id IS NULL THEN 1 ELSE 0 END) AS null_user_cnt
    FROM user_behavior
""")
result.show()

# 检查行为类型枚举
spark.sql("""
    SELECT behavior_type, COUNT(*) AS cnt
    FROM user_behavior
    GROUP BY behavior_type
    ORDER BY cnt DESC
""").show()
