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