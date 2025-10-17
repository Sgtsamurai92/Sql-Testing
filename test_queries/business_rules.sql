-- Orders marked 'Paid' must have an associated payment record
SELECT o.order_id
FROM orders o
LEFT JOIN payments p ON o.order_id = p.order_id
WHERE o.status = 'Paid' AND p.payment_id IS NULL;

-- Payments must not exceed $10,000
SELECT payment_id, amount FROM payments WHERE amount > 10000;