-- =======================
-- INSERCIÓN DE LAS TABLAS
-- =======================

PRAGMA table_info(products);

-- ================
-- TABLA DE HECHOS
-- ================

INSERT INTO fact_sales
SELECT
    od.order_id,
    o.order_date,
    od.product_id,
    p.category_id,
    o.region_id,
    od.sales
FROM order_details od
JOIN orders o ON od.order_id = o.order_id
JOIN products p ON od.product_id = p.product_id;

-- =============================
-- Inserción de las dimensiones
-- =============================

DELETE FROM dim_date;
INSERT OR IGNORE INTO dim_date
SELECT DISTINCT
    date(
        substr(order_date, 7, 4) || '-' ||
        substr(order_date, 4, 2) || '-' ||
        substr(order_date, 1, 2)
    ) AS order_date,
    CAST(strftime('%Y',
        date(substr(order_date, 7, 4) || '-' ||
             substr(order_date, 4, 2) || '-' ||
             substr(order_date, 1, 2))
    ) AS INTEGER) AS year,
    CAST(strftime('%m',
        date(substr(order_date, 7, 4) || '-' ||
             substr(order_date, 4, 2) || '-' ||
             substr(order_date, 1, 2))
    ) AS INTEGER) AS month,
    CAST(strftime('%d',
        date(substr(order_date, 7, 4) || '-' ||
             substr(order_date, 4, 2) || '-' ||
             substr(order_date, 1, 2))
    ) AS INTEGER) AS day
FROM orders
WHERE order_date IS NOT NULL;


SELECT * FROM dim_date;

INSERT INTO dim_product
SELECT DISTINCT
    product_id,
    category_id
FROM products;


INSERT INTO dim_category
SELECT DISTINCT
    category_id,
    category,
    sub_category
FROM categories;



INSERT INTO dim_region
SELECT DISTINCT
    region_id,
    region
FROM regions;
