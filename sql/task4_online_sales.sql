-- Q4: How many sales are coming from the online store?
-- 	The company is looking to increase its online sales.
-- 	They want to know how many sales are happening online vs offline.
-- 	Calculate how many products were sold and the amount of sales made for online and offline purchases.

-- 	You should get the following information:
-- 	+------------------+-------------------------+----------+
-- 	| numbers_of_sales | product_quantity_count  | location |
-- 	+------------------+-------------------------+----------+
-- 	|            26957 |                  107739 | Web      |
-- 	|            93166 |                  374047 | Offline  |
-- 	+------------------+-------------------------+----------+

SELECT
	COUNT(orders_table.product_code) AS number_of_sales,
	SUM(product_quantity) AS product_quantity_count,
	CASE
		WHEN store_type LIKE '%Web%' THEN 'Web'
		ELSE 'Offline'
	END AS location
FROM 
	orders_table
JOIN 
	dim_store_details on dim_store_details.store_code = orders_table.store_code
GROUP BY 
	location
ORDER BY
	location DESC
	
----------- OUTPUT -----------

-- 	"number_of_sales"	"product_quantity_count"	  "location"
-- 		26957				107739						"Web"
-- 		93166				374047						"Offline"