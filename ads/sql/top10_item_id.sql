-- 热门商品TOP10 
SELECT item_id , COUNT(*) AS all_behavior_cnt
FROM user_behavior
GROUP BY item_id
ORDER BY all_behavior_cnt DESC
LIMIT 10; 