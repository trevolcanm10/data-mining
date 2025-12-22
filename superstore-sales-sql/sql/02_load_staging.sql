-- ================================
-- Paso 0: Activar integridad referencial
-- ================================
PRAGMA foreign_keys = ON;

---================================
--- Poblar categories
---================================
INSERT INTO categories (category,sub_category)
SELECT DISTINCT category, sub_category
FROM staging_superstore;

---=======================
--- Poblar Regions
---=======================
INSERT INTO regions (country,region,state,city,postal_code)
SELECT DISTINCT country, region , state , city , postal_code
FROM staging_superstore;

---=======================
--- Poblar Customers
---=======================
INSERT INTO customers (customer_id,customer_name,segment)
SELECT DISTINCT customer_id, customer_name, segment
FROM staging_superstore;

---=======================
--- Poblar products
---=======================
INSERT INTO products (product_id,product_name,category_id)
SELECT s.product_id, s.product_name , c.category_id
FROM staging_superstore s
JOIN categories c ON s.category = c.category
AND s.sub_category = c.sub_category
GROUP BY s.product_id;

---=======================
--- Poblar Orders
---=======================
INSERT INTO orders(order_id,order_date,ship_date,ship_mode,customer_id,region_id)
SELECT s.order_id, s.order_date, s.ship_date, s.ship_mode, s.customer_id,r.region_id
FROM staging_superstore s
JOIN regions r 
ON s.country =  r.country
AND s.region = r.region
AND s.state = r.state
AND s.city = r.city
AND s.postal_code = r.postal_code
GROUP BY s.order_id;


===============================
---Poblar order_details(HECHOS)
===============================
INSERT INTO order_details(row_id,order_id,product_id,sales)
SELECT row_id, order_id, product_id, sales
FROM staging_superstore;

---Conteos Básicos
SELECT COUNT(*) FROM order_details;
SELECT COUNT(*) FROM orders;
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM products;

---Veremos las 5 filas de la tabla de hechos
SELECT * FROM order_details LIMIT 5;