
---

## **schema/create_tables.sql**
```sql```
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS payments;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    product_name TEXT NOT NULL,
    quantity INTEGER CHECK (quantity > 0),
    status TEXT CHECK (status IN ('Pending', 'Paid', 'Cancelled')),
    FOREIGN KEY (customer_id) REFERENCES users(user_id)
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    amount REAL CHECK (amount > 0),
    payment_date TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
