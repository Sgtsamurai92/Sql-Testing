-- Verify product names are not empty
SELECT order_id FROM orders WHERE product_name = '';

-- Ensure all quantities are greater than 0
SELECT order_id FROM orders WHERE quantity <= 0;