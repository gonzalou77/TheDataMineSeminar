-- name: get_title
-- Get many types of information from the database
SELECT primary_title, premiered, runtime_minutes FROM titles WHERE title_id = :title_id;

