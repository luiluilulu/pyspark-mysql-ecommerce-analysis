-- 每日浏览量和浏览用户数
SELECT behavior_date,COUNT(*) AS pv_cnt,COUNT(DISTINCT user_id) AS user_cnt
FROM user_behavior
WHERE behavior_type='pv'
GROUP BY behavior_date
ORDER BY behavior_date;