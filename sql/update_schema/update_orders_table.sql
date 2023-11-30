SELECT * FROM orders_table;

-- View current data types for all columns in the table using information_schema
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'orders_table';

/*  Check the maximum lengths of exisitng data for the text columns. 
	Then set the VARCHAR sizes to accomodate them	*/

-- Check the maximum length of card_number
SELECT MAX(CHAR_LENGTH(card_number)) FROM orders_table;
-- 19

-- Check the maximum length of store_code
SELECT MAX(CHAR_LENGTH(store_code)) FROM orders_table;
-- 12

-- Check the maximum length of product_code
SELECT MAX(CHAR_LENGTH(product_code)) FROM orders_table;
-- 11

-- Set the data types for all columns

-- Change data type of date_uuid to UUID
ALTER TABLE orders_table
ALTER COLUMN date_uuid TYPE UUID
USING date_uuid::UUID;

-- Change data type of user_uuid to UUID
ALTER TABLE orders_table
ALTER COLUMN user_uuid TYPE UUID
USING user_uuid::UUID;

-- Change data type of card_number to VARCHAR with a maximum length of 24
ALTER TABLE orders_table
ALTER COLUMN card_number TYPE VARCHAR(24);

-- Change data type of store_code to VARCHAR with a maximum length of 16
ALTER TABLE orders_table
ALTER COLUMN store_code TYPE VARCHAR(16);

-- Change data type of product_code to VARCHAR with a maximum length of 16
ALTER TABLE orders_table
ALTER COLUMN product_code TYPE VARCHAR(16);

-- Change data type of product_quantity to SMALLINT
ALTER TABLE orders_table
ALTER COLUMN product_quantity TYPE SMALLINT;

-- DELETE extra columns
ALTER TABLE orders_table
DROP COLUMN level_0;

-- Create Foreign key constraints
ALTER TABLE orders_table
ADD CONSTRAINT FK_orders_table_dim_date_times_date_uuid
FOREIGN KEY (date_uuid)
REFERENCES dim_date_times(date_uuid);

ALTER TABLE orders_table
ADD CONSTRAINT FK_orders_table_dim_users_user_uuid
FOREIGN KEY (user_uuid)
REFERENCES dim_users(user_uuid);

ALTER TABLE orders_table
ADD CONSTRAINT FK_orders_table_dim_card_details_card_number
FOREIGN KEY (card_number)
REFERENCES dim_card_details(card_number);

ALTER TABLE orders_table
ADD CONSTRAINT FK_orders_table_dim_store_details_store_code
FOREIGN KEY (store_code)
REFERENCES dim_store_details(store_code);

ALTER TABLE orders_table
ADD CONSTRAINT FK_orders_table_dim_products_product_code
FOREIGN KEY (product_code)
REFERENCES dim_products(product_code);