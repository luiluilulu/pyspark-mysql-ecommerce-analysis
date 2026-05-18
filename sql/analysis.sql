-- 总行数
SELECT COUNT(*) AS total_cnt FROM user_behavior;

-- 总用户数
SELECT COUNT(DISTINCT user_id) AS user_cnt FROM user_behavior;

-- 总商品数
SELECT COUNT(DISTINCT item_id) AS item_cnt FROM user_behavior;

-- 看各类行为的数量,降序排序
SELECT behavior_type , COUNT(*) AS cnt
FROM user_behavior
GROUP BY behavior_type
ORDER BY COUNT(*) DESC;

-- 每日浏览量和浏览用户数
SELECT behavior_date,COUNT(*) AS pv_cnt,COUNT(DISTINCT user_id) AS user_cnt
FROM user_behavior
WHERE behavior_type='pv'
GROUP BY behavior_date
ORDER BY behavior_date;

-- 每小时行为量
SELECT behavior_hour, COUNT(*) AS behavior_cnt
FROM user_behavior
GROUP BY behavior_hour
ORDER BY behavior_hour;

-- 购买王(前十名)
SELECT user_id,COUNT(*) AS buy_cnt
FROM user_behavior
WHERE behavior_type='buy'
GROUP BY user_id
ORDER BY buy_cnt DESC
LIMIT 10;

-- 热门商品TOP10 
SELECT item_id , COUNT(*) AS all_behavior_cnt
FROM user_behavior
GROUP BY item_id
ORDER BY all_behavior_cnt DESC
LIMIT 10; 

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

-- 类目热度分析
SELECT 
    category_id,
    COUNT(*) AS behavior_cnt,
    COUNT(CASE WHEN behavior_type = 'pv' THEN 1 END) AS pv_cnt,
    COUNT(CASE WHEN behavior_type IN ('fav','cart') THEN 1 END ) AS cart_fav_cnt,
    COUNT(CASE WHEN behavior_type = 'buy' THEN 1 END) AS buy_cnt,
    COUNT(DISTINCT CASE WHEN behavior_type = 'buy' THEN user_id END) AS buy_user_cnt

FROM user_behavior
GROUP BY category_id
ORDER BY behavior_cnt DESC
LIMIT 10;
