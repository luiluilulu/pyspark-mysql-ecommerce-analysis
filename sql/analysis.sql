-- 总行数
SELECT COUNT(*) FROM user_behavior;

-- 看各类行为的数量
SELECT behavior_type , COUNT(*) AS cnt
FROM user_behavior
GROUP BY behavior_type;

-- 每日行为量
SELECT behavior_date,COUNT(*) AS cnt
FROM user_behavior
GROUP BY behavior_date
ORDER BY behavior_date;

-- 每小时行为量
SELECT behavior_hour, COUNT(*) AS cnt
FROM user_behavior
GROUP BY behavior_hour
ORDER BY behavior_hour;