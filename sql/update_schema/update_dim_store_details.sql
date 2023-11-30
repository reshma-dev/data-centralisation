SELECT * FROM dim_store_details;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dim_store_details';

SELECT MAX(CHAR_LENGTH(store_code)) FROM dim_store_details;
-- 12

SELECT MAX(CHAR_LENGTH(country_code)) FROM dim_store_details;
-- 2

-- Change data type of longitude to FLOAT
ALTER TABLE dim_store_details
ALTER COLUMN longitude TYPE FLOAT;

-- Change data type of locality to VARCHAR(255)
ALTER TABLE dim_store_details
ALTER COLUMN locality TYPE VARCHAR(255);

-- Change data type of store_code to VARCHAR(16)
ALTER TABLE dim_store_details
ALTER COLUMN store_code TYPE VARCHAR(16);

-- Change data type of staff_numbers to SMALLINT
ALTER TABLE dim_store_details
ALTER COLUMN staff_numbers TYPE SMALLINT;

-- Change data type of opening_date to DATE
ALTER TABLE dim_store_details
ALTER COLUMN opening_date TYPE DATE
USING opening_date::DATE;

-- Change data type of store_type to VARCHAR(255) NULL values are allowed
ALTER TABLE dim_store_details
ALTER COLUMN store_type SET DATA TYPE VARCHAR(255), 
ALTER COLUMN store_type DROP NOT NULL;

-- Change data type of latitude to FLOAT
ALTER TABLE dim_store_details
ALTER COLUMN latitude TYPE FLOAT;

-- Change data type of country_code to VARCHAR(4)
ALTER TABLE dim_store_details
ALTER COLUMN country_code TYPE VARCHAR(4);

-- Change data type of continent to VARCHAR(255)
ALTER TABLE dim_store_details
ALTER COLUMN continent TYPE VARCHAR(255);

-- DROP extra column created during data processing in python that was left in
ALTER TABLE dim_store_details
DROP COLUMN staff_numbers_tmp;

-- Add Primary key
ALTER TABLE dim_store_details
ADD PRIMARY KEY (store_code);