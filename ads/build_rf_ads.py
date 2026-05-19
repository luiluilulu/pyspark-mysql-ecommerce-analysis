from utils.spark_utils import create_spark,write_df_to_mysql
from utils.path_utils import CLEANED_DATA_PATH
from utils.config_utils import MYSQL_CONFIG,get_jdbc_url

spark  = create_spark('BuildRfAds',with_mysql=True)

df = spark.read.parquet(str(CLEANED_DATA_PATH))
df.createOrReplaceTempView("user_behavior")
#先做RF
result_df = spark.sql(""" 
    WITH analysis_date AS(
    SELECT MAX(behavior_date) AS max_date
    FROM user_behavior
),
user_buy_summary AS (
    SELECT
        user_id,
        MAX(behavior_date) AS user_latest_buy_date,
        COUNT(*) AS user_buy_cnt
    FROM user_behavior
    WHERE behavior_type = 'buy'
    GROUP BY user_id
),
user_rf AS (
    SELECT
        user_id,
        DATEDIFF(ad.max_date,ubs.user_latest_buy_date) AS user_latest_buy_datediff,
        user_buy_cnt
    FROM user_buy_summary AS ubs
    CROSS JOIN analysis_date AS ad
),
user_R_distribute AS(
    SELECT 
        user_latest_buy_datediff,
        NTILE(4) OVER (ORDER BY user_latest_buy_datediff) AS r_quartile
    FROM user_rf
),
user_rf_segment AS (
    SELECT
        user_id,
        user_buy_cnt,
        CASE 
            WHEN user_latest_buy_datediff <=3 AND user_buy_cnt>=2 THEN '高价值用户'
            WHEN user_latest_buy_datediff <=3 AND user_buy_cnt = 1 THEN '最近购买用户'
            WHEN user_latest_buy_datediff >3 AND user_buy_cnt>=2 THEN '沉默复购用户'
            ELSE '普通购买用户'
        END AS user_segment
    FROM user_rf
)
SELECT 
    r_quartile,
    count(*) as user_cnt
FROM user_R_distribute
GROUP BY r_quartile
ORDER BY r_quartile;


"""
)

write_df_to_mysql(result_df,"ads_rf_recency_quartile")

spark.stop()
