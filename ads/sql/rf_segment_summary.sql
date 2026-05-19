-- RF
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
        DATEDIFF(ad.max_date,ubs.user_latest_buy_date) AS recency_days,
        user_buy_cnt
    FROM user_buy_summary AS ubs
    CROSS JOIN analysis_date AS ad
),
user_rf_segment AS (
    SELECT
        user_id,
        user_buy_cnt,
        CASE 
            WHEN recency_days <=2 AND user_buy_cnt>=2 THEN '高价值用户'
            WHEN recency_days <=2 AND user_buy_cnt = 1 THEN '最近购买用户'
            WHEN recency_days >2 AND user_buy_cnt>=2 THEN '沉默复购用户'
            ELSE '普通购买用户'
        END AS user_segment
    FROM user_rf
)
SELECT 
    user_segment,
    COUNT(*) AS user_cnt
FROM user_rf_segment
GROUP BY user_segment
ORDER BY user_cnt DESC;