-- Check for missing customer IDs
SELECT order_id FROM orders WHERE customer_id IS NULL;

-- Check for duplicate emails
SELECT email, COUNT(*) 
FROM users
GROUP BY email
HAVING COUNT(*) > 1;