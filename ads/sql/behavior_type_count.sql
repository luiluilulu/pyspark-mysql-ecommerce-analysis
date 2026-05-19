-- 看各类行为的数量,降序排序
SELECT behavior_type , COUNT(*) AS cnt
FROM user_behavior
GROUP BY behavior_type
ORDER BY COUNT(*) DESC;
