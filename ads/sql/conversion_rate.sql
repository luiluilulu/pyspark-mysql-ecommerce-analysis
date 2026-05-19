-- 转化率漏斗

WITH user_stage_flag AS(
    SELECT
        user_id,
        MAX(CASE WHEN behavior_type = 'pv' THEN 1 ELSE 0 END) AS has_pv,
        MAX(CASE WHEN behavior_type IN ('fav','cart') THEN 1 ELSE 0 END) AS has_cart_or_fav,
        MAX(CASE WHEN behavior_type = 'buy' THEN 1 ELSE 0 END) AS has_buy
    FROM user_behavior
    GROUP BY user_id
),
funnel_user_cnt AS(
    SELECT 
        COUNT(CASE WHEN has_pv = 1 THEN 1 END) AS pv_user_cnt,
        COUNT(CASE WHEN has_pv=1 AND has_cart_or_fav = 1  THEN 1 END) AS cart_fav_user_cnt,
        COUNT(CASE WHEN has_pv =1 AND has_cart_or_fav =1 AND has_buy =1 THEN 1 END) AS buy_user_cnt
    FROM user_stage_flag
),
conversion_rate AS (
    SELECT
        1 AS step_order,
        '浏览->收藏/加购' AS step,
        pv_user_cnt AS start_users,
        cart_fav_user_cnt AS converted_users,
        CASE
            WHEN pv_user_cnt = 0 THEN 0
            ELSE ROUND(cart_fav_user_cnt *100.0 / pv_user_cnt,2)
            END AS rate
    FROM funnel_user_cnt
    UNION ALL
    SELECT
        2 AS step_order,
        '收藏/加购->购买' AS step,
        cart_fav_user_cnt AS start_users,
        buy_user_cnt AS converted_users,
        CASE
            WHEN cart_fav_user_cnt = 0 THEN 0
            ELSE ROUND(buy_user_cnt *100.0 / cart_fav_user_cnt,2)
            END AS rate
    FROM funnel_user_cnt
)

SELECT *
FROM conversion_rate;