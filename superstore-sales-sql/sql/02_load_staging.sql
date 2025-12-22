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

