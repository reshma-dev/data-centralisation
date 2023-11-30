SELECT * FROM dim_products;

UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '')
WHERE product_price LIKE '£%';

ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(20);

UPDATE dim_products
SET weight_class =
	CASE
		WHEN weight < 2 THEN 'Light'
		WHEN weight >=2 AND weight < 40 THEN 'Mid_Sized'
		WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
		WHEN weight >= 140 THEN 'Truck_Required'
	END;
	

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dim_products';


ALTER TABLE dim_products
RENAME COLUMN removed to still_available;


SELECT MAX(CHAR_LENGTH("EAN")) FROM dim_products;
-- 17

SELECT MAX(CHAR_LENGTH(product_code)) FROM dim_products;
-- 11 -> the column is set to 16 in orders table

SELECT MAX(CHAR_LENGTH(weight_class)) FROM dim_products;
-- 14

-- To be able to change the column type to boolean, update content with true or false
UPDATE dim_products
SET still_available =
	CASE
		WHEN still_available = 'Still_avaliable' THEN true
		WHEN still_available = 'Removed' THEN false
	END;

ALTER TABLE dim_products
ALTER COLUMN product_price TYPE FLOAT
USING product_price::FLOAT;
--USING product_price::double precision;

ALTER TABLE dim_products
ALTER COLUMN weight TYPE FLOAT
USING weight::FLOAT;

-- NOTE: As the column name is in Capital letters, it had to be specified in double quotes 
ALTER TABLE dim_products
ALTER COLUMN "EAN" TYPE VARCHAR(24);

ALTER TABLE dim_products
ALTER COLUMN product_code TYPE VARCHAR(16);

ALTER TABLE dim_products
ALTER COLUMN date_added TYPE DATE;

ALTER TABLE dim_products
ALTER COLUMN uuid TYPE UUID
USING uuid::UUID;

ALTER TABLE dim_products
ALTER COLUMN still_available TYPE BOOL
USING still_available::boolean;

ALTER TABLE dim_products
ALTER COLUMN weight_class TYPE VARCHAR(16);


ALTER TABLE dim_products
ADD PRIMARY KEY (product_code);
