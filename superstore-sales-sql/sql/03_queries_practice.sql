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
PRAGMA table_info(orders);

SELECT * FROM orders;