-- ================================
-- Tabla: customers
-- ================================
CREATE TABLE customers(
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT,
    segment TEXT
);

CREATE TABLE regions(
    region_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT,
    region TEXT,
    state TEXT,
    city TEXT,
    postal_code TEXT
);

CREATE TABLE categories(
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    sub_category TEXT
);

CREATE TABLE products(
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)

);

CREATE TABLE orders(
    order_id TEXT PRIMARY KEY,
    order_date DATE,
    ship_date DATE,
    ship_mode TEXT,
    customer_id TEXT,
    region_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);

-- ============================
-- TABLA DE HECHOS
-- ============================

CREATE TABLE order_details(
    row_id INTEGER PRIMARY KEY,
    order_id TEXT,
    product_id TEXT,
    sales REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

