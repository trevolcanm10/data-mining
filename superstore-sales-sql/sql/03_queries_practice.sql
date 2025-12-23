---Consultas claves

--Ventas Totales
SELECT ROUND(SUM(sales),2) AS total_sales
FROM order_details;

--Ventas por categoria
SELECT c.category,
        ROUND(SUM(od.sales),2) AS total_sales
FROM order_details od
JOIN products p ON od.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category
ORDER BY total_sales DESC;

--TOP DE 10 CLIENTES POR VENTAS
SELECT cu.customer_name, ROUND(SUM(od.sales),2) AS total_sales
FROM order_details od
JOIN orders o ON o.order_id = od.order_id
JOIN customers cu ON o.customer_id = cu.customer_id
GROUP BY cu.customer_name
ORDER BY total_sales DESC
LIMIT 10;

--VENTAS POR REGION
SELECT r.region, ROUND(SUM(od.sales),2) AS total_sales
FROM order_details od
JOIN orders o ON od.order_id = o.order_id
JOIN regions r ON o.region_id = r.region_id
GROUP BY r.region
ORDER BY total_sales DESC;

--TENDENCIAS DE VENTAS POR AÑO
SELECT substr(o.order_date,7,4) AS year,
        ROUND(SUM(od.sales),2) AS total_sales
FROM order_details od 
JOIN orders o ON od.order_id = o.order_id
GROUP BY year
ORDER BY year;



SELECT sales FROM order_details;
--RANKING  DE PRODUCTOS POR VENTAS
SELECT p.product_name,
        ROUND(SUM(od.sales),2) total_sales,
        RANK() OVER(ORDER BY SUM(od.sales) DESC) AS sales_rank
FROM order_details od
JOIN products p ON od.product_id = p.product_id
GROUP BY product_name
ORDER BY sales_rank;

--TOP Producto por Categoría
WITH product_sales AS(
        SELECT
                c.category,
                p.product_name,
                SUM(od.sales) AS total_sales,
                RANK() OVER ( PARTITION BY c.category
                ORDER BY SUM(od.sales) DESC
                ) AS rank_in_category
        FROM order_details od
        JOIN products p ON od.product_id = p.product_id
        JOIN categories c ON p.category_id = c.category_id
        GROUP BY c.category,p.product_name
)
SELECT * FROM product_sales
WHERE rank_in_category = 1;

--Participación (%) de cada categoría en ventas totales
WITH total_sales AS (
        SELECT SUM(sales) AS total FROM order_details
)
SELECT
        c.category,
        ROUND(SUM(od.sales),2) AS category_sales,
        ROUND(100.0 * SUM(od.sales) / (SELECT total FROM total_sales),2) AS percentage_of_total
FROM order_details od
JOIN products p ON od.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category
ORDER BY percentage_of_total DESC;

SELECT * FROM orders;

--Clientes que concentran el 80% de las ventas
WITH customer_sales AS(
        SELECT
                cu.customer_name,
                SUM(od.sales) AS total_sales
        FROM order_details od
        JOIN orders o ON od.order_id = o.order_id
        JOIN customers cu ON o.customer_id = cu.customer_id
        GROUP BY cu.customer_name
),

running_total AS(
        SELECT
                customer_name,
                total_sales,
                
)

PRAGMA table_info(orders);
