-- 每小时行为量
SELECT behavior_hour, COUNT(*) AS behavior_cnt
FROM user_behavior
GROUP BY behavior_hour
ORDER BY behavior_hour;