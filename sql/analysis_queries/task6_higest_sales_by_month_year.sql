-- 	Q6: Which month in each year produced the highest cost of sales?
-- 		The company stakeholders want assurances that the company has been doing well recently.
-- 		Find which months in which years have had the most sales historically.
-- 	The query should return the following information:

-- 	+-------------+------+-------+
-- 	| total_sales | year | month |
-- 	+-------------+------+-------+
-- 	|    27936.77 | 1994 |     3 |
-- 	|    27356.14 | 2019 |     1 |
-- 	|    27091.67 | 2009 |     8 |
-- 	|    26679.98 | 1997 |    11 |
-- 	|    26310.97 | 2018 |    12 |
-- 	|    26277.72 | 2019 |     8 |
-- 	|    26236.67 | 2017 |     9 |
-- 	|    25798.12 | 2010 |     5 |
-- 	|    25648.29 | 1996 |     8 |
-- 	|    25614.54 | 2000 |     1 |
-- 	+-------------+------+-------+

SELECT 
	ROUND(SUM(product_price * product_quantity)::NUMERIC, 2) as total_sales,
	year,
	month
FROM
	orders_table
JOIN
	dim_date_times on dim_date_times.date_uuid = orders_table.date_uuid
JOIN
	dim_products on dim_products.product_code = orders_table.product_code
GROUP BY
	year, month
ORDER BY 
	total_sales DESC
LIMIT
	10;
	
--------------- OUTPUT -------------------
	"total_sales"	"year"	"month"
		27936.77	"1994"	"3"
		27356.14	"2019"	"1"
		27091.67	"2009"	"8"
		26679.98	"1997"	"11"
		26310.97	"2018"	"12"
		26277.72	"2019"	"8"
		26236.67	"2017"	"9"
		25798.12	"2010"	"5"
		25648.29	"1996"	"8"
		25614.54	"2000"	"1"