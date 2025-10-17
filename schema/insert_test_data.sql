INSERT INTO users (name, email) VALUES
('Alice', 'alice@example.com'),
('Bob', 'bob@example.com'),
('Charlie', 'charlie@example.com');

INSERT INTO orders (customer_id, product_name, quantity, status) VALUES
(1, 'Laptop', 1, 'Paid'),
(2, 'Headphones', 2, 'Pending'),
(3, 'Keyboard', 1, 'Paid'),
(NULL, 'Mouse', 1, 'Paid'); -- Intentional error for testing

INSERT INTO payments (order_id, amount, payment_date) VALUES
(1, 999.99, '2025-10-17');
-- Missing payment for order_id 3 to trigger a test failure