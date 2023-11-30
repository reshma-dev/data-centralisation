-- Q3: Which months produced the largest amount of sales?
-- 	Query the database to find out which months have produced the most sales. 
--	The query should return the following information:
-- +-------------+-------+
-- | total_sales | month |
-- +-------------+-------+
-- |   673295.68 |     8 |
-- |   668041.45 |     1 |
-- |   657335.84 |    10 |
-- |   650321.43 |     5 |
-- |   645741.70 |     7 |
-- |   645463.00 |     3 |
-- +-------------+-------+

SELECT 
	ROUND(SUM(product_price * product_quantity)::NUMERIC, 2) AS total_sales, 
	month
FROM 
	orders_table
JOIN 
	dim_products on dim_products.product_code = orders_table.product_code
JOIN 
	dim_date_times on dim_date_times.date_uuid = orders_table.date_uuid
GROUP BY
	month
ORDER BY
	total_sales DESC
LIMIT
	6;
	
-------- OUTPUT ---------

-- 	"total_sales"	"month"
-- 	673295.68		"8"
-- 	668041.45		"1"
-- 	657335.84		"10"
-- 	650321.43		"5"
-- 	645741.70		"7"
-- 	645463.00		"3"
