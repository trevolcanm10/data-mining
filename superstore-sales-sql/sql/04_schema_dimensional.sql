-- ============================
-- TABLA DE HECHOS
-- ============================

CREATE TABLE fact_sales(
    order_id TEXT,
    order_date DATE,
    product_id TEXT,
    category_id TEXT,
    region_id INTEGER,
    sales REAL
);


-- =============
-- DIMENSIONES
-- =============

CREATE TABLE dim_date(
    order_date DATE PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    day INTEGER
);

CREATE TABLE dim_product(
    product_id TEXT PRIMARY KEY,
    category_id TEXT
);

CREATE TABLE dim_category(
    category_id TEXT PRIMARY KEY,
    category TEXT,
    sub_category TEXT
);


CREATE TABLE dim_region(
    region_id INTEGER PRIMARY KEY,
    region TEXT
);
