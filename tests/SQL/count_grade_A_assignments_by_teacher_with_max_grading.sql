-- -- Write query to find the number of grade A's given by the teacher who has graded the most assignments
-- WITH teacher_assignment_count AS (
--     -- SELECT teacher_id, COUNT(*) AS total_assignments
--     -- FROM assignments
--     -- WHERE state = 'GRADED'  -- Assuming assignments must be in a graded state
--     -- GROUP BY teacher_id
--     SELECT teacher_id, grade, COUNT(*) AS count
--     FROM assignments
--     WHERE state = 'GRADED'
--     GROUP BY teacher_id, grade;
-- ),
-- top_teacher AS (
--     SELECT teacher_id
--     FROM teacher_assignment_count
--     ORDER BY total_assignments DESC
--     LIMIT 1
-- )
-- SELECT COUNT(*) AS grade_a_count
-- FROM assignments
-- WHERE grade = 'A'
--   AND teacher_id = (SELECT teacher_id FROM top_teacher);


WITH teacher_assignment_count AS (
    SELECT teacher_id, COUNT(*) AS total_assignments
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
),
top_teacher AS (
    SELECT teacher_id
    FROM teacher_assignment_count
    ORDER BY total_assignments DESC
    LIMIT 1
)
SELECT COUNT(*) AS grade_a_count
FROM assignments
WHERE grade = 'A'
  AND teacher_id = (SELECT teacher_id FROM top_teacher);
