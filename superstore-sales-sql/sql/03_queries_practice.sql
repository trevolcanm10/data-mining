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
                SUM(total_sales) OVER (ORDER BY total_sales DESC) AS cumulative_sales,
                SUM(total_sales) OVER () AS overall_sales
        FROM customer_sales
)
SELECT
        customer_name,
        ROUND(total_sales,2) AS total_sales,
        ROUND(100.0 * cumulative_sales / overall_sales,2) AS cumulative_percentage
FROM running_total
WHERE cumulative_sales <= overall_sales * 0.8;

--Ventas promedio por pedido
SELECT
        ROUND(AVG(order_total),2) AS avg_sales_per_oder
FROM(
        SELECT
                o.order_id,
                SUM(od.sales) AS order_total
        FROM order_details od 
        JOIN orders o ON od.order_id = o.order_id
        GROUP BY o.order_id

);
PRAGMA table_info(orders);

--Dias con mayores ventas
SELECT
        o.order_date,
        ROUND(SUM(od.sales),2) AS daily_sales
FROM order_details od 
JOIN orders o ON od.order_id = o.order_id
GROUP BY o.order_date
ORDER BY daily_sales DESC
LIMIT 10;

--Querie para exportar CSV a Power BI
SELECT  
        o.order_id,
        o.order_date,
        c.category,
        c.sub_category,
        r.region,
        od.sales
FROM order_details od 
JOIN orders o ON od.order_id = o.order_id
JOIN products p  ON od.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
JOIN regions r ON o.region_id = r.region_id;

