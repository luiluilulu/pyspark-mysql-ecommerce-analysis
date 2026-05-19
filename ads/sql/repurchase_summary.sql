-- 复购
WITH user_buy_cnt AS (
    SELECT 
        user_id,
        COUNT(*) AS buy_cnt
    FROM user_behavior
    WHERE behavior_type = 'buy'
    GROUP BY user_id
),
repurchase_summary AS (
    SELECT
        COUNT(*) AS buy_user_cnt,
        COUNT(CASE WHEN buy_cnt >=2 THEN 1 END) AS repurchase_user_cnt
    FROM user_buy_cnt
    )

SELECT
    buy_user_cnt,
    repurchase_user_cnt,
    ROUND(
        CASE 
            WHEN buy_user_cnt = 0 THEN 0
            ELSE repurchase_user_cnt *100.0 / buy_user_cnt
        END,
        2)  AS repurchase_rate
FROM repurchase_summary;