--  Q5: What percentage of sales come through each type of store?
-- 	The sales team wants to know which of the different store types is generated the most revenue so they know where to focus.
-- 	Find out the total and percentage of sales coming from each of the different store types.

-- 	The query should return:

-- 	+-------------+-------------+---------------------+
-- 	| store_type  | total_sales | percentage_total(%) |
-- 	+-------------+-------------+---------------------+
-- 	| Local       |  3440896.52 |               44.87 |
-- 	| Web portal  |  1726547.05 |               22.44 |
-- 	| Super Store |  1224293.65 |               15.63 |
-- 	| Mall Kiosk  |   698791.61 |                8.96 |
-- 	| Outlet      |   631804.81 |                8.10 |
-- 	+-------------+-------------+---------------------+

WITH 
	cte_sales_by_store_type AS (
		SELECT 
			store_type,
			ROUND( SUM( product_price * product_quantity )::NUMERIC, 2) AS total_sales
		FROM 
			orders_table
		JOIN
			dim_store_details on dim_store_details.store_code = orders_table.store_code
		JOIN
			dim_products on dim_products.product_code = orders_table.product_code
		GROUP BY
			store_type
	), 
	cte_grand_total AS (
		SELECT
			SUM(total_sales) AS revenue
		FROM
			cte_sales_by_store_type
	)
SELECT
	store_type,
	total_sales,
	ROUND( total_sales * 100 / cte_grand_total.revenue, 2 ) as percentage_total
FROM
	cte_sales_by_store_type, cte_grand_total
ORDER BY
	total_sales DESC;


---------------------- OUTPUT ----------------------------------

-- 	  "store_type"		  "total_sales"		"percentage_total"
-- 		"Local"				3440896.52			44.56
-- 		"Web Portal"		1726547.05			22.36
-- 		"Super Store"		1224293.65			15.85
-- 		"Mall Kiosk"		 698791.61			 9.05
-- 		"Outlet"			 631804.81			 8.18

