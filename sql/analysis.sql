-- 总行数
SELECT COUNT(*) AS total_cnt FROM user_behavior;

--总用户数
SELECT COUNT(DISTINCT user_id) AS user_cnt FROM user_behavior;

--总商品数
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

--购买王(前十名)
SELECT user_id,COUNT(*) AS buy_cnt
FROM user_behavior
WHERE behavior_type='buy'
GROUP BY user_id
ORDER BY buy_cnt DESC
LIMIT 10;

--热门商品TOP10 
SELECT item_id , COUNT(*) AS all_behavior_cnt
FROM user_behavior
GROUP BY item_id
ORDER BY all_behavior_cnt DESC
LIMIT 10; 