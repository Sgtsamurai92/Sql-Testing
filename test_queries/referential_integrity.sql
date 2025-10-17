-- Orders must have valid customer IDs
SELECT order_id
FROM orders
WHERE customer_id NOT IN (SELECT user_id FROM users);