SELECT * FROM dim_card_details;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dim_card_details';

SELECT MAX(CHAR_LENGTH(card_number)) FROM dim_card_details;
-- 19 -- set to 24 in orders table

SELECT MAX(CHAR_LENGTH(expiry_date)) FROM dim_card_details;
-- 5

-- Set data types to columns
ALTER TABLE dim_card_details
ALTER COLUMN card_number TYPE VARCHAR(24);

ALTER TABLE dim_card_details
ALTER COLUMN expiry_date TYPE VARCHAR(6);

ALTER TABLE dim_card_details
ALTER COLUMN date_payment_confirmed TYPE DATE
Using date_payment_confirmed::DATE;

-- Set Primary key
ALTER TABLE dim_card_details
ADD PRIMARY KEY (card_number);

--- check if pkey got applied
SELECT
    *
FROM
    information_schema.key_column_usage
WHERE
    table_name = 'dim_card_details'
    AND column_name = 'card_number';

    
