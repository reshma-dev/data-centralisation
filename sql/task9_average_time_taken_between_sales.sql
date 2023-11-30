-- 	Q9: How quickly is the company making sales?
-- 		Sales would like the get an accurate metric for how quickly the company is making sales.

-- 	Determine the average time taken between each sale grouped by year, the query should return the following information:

-- 	 +------+-------------------------------------------------------+
-- 	 | year |                           actual_time_taken           |
-- 	 +------+-------------------------------------------------------+
-- 	 | 2013 | "hours": 2, "minutes": 17, "seconds": 12, "millise... |
-- 	 | 1993 | "hours": 2, "minutes": 15, "seconds": 35, "millise... |
-- 	 | 2002 | "hours": 2, "minutes": 13, "seconds": 50, "millise... | 
-- 	 | 2022 | "hours": 2, "minutes": 13, "seconds": 6,  "millise... |
-- 	 | 2008 | "hours": 2, "minutes": 13, "seconds": 2,  "millise... |
-- 	 +------+-------------------------------------------------------+

WITH 
	cte_get_timestamp AS(
		SELECT
		year,
		to_timestamp(CONCAT(year, '-', month, '-', day, ' ', timestamp), 'YYYY-MM-DD hh24:mi:ss')::timestamp as tt
	FROM dim_date_times
	GROUP BY
		year, month, day, timestamp
	ORDER BY
		year, month, day DESC	
	),
	cte_time_diff As (
	SELECT
		year,
		LEAD (tt) OVER( ORDER BY tt ) - tt AS diff
		FROM cte_get_timestamp
	)
SELECT 	
	year, 
	AVG(diff) as actual_time_taken
FROM
	cte_time_diff
GROUP BY
 	year
ORDER BY
 	actual_time_taken DESC
LIMIT
	5;
	
--------------- OUTPUT ---------------

-- 	"year"	"actual_time_taken"
-- 	"2013"	"02:17:15.655442"
-- 	"1993"	"02:15:42.230194"
-- 	"2002"	"02:13:51.523434"
-- 	"2008"	"02:13:03.532442"
-- 	"2022"	"02:13:02.003698"