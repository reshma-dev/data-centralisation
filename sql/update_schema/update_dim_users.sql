SELECT * FROM dim_users;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dim_users';

SELECT MAX(CHAR_LENGTH(country_code)) FROM dim_users;
-- 3

-- Change data type of first_name to VARCHAR(255)
ALTER TABLE dim_users
ALTER COLUMN first_name TYPE VARCHAR(255);

-- Change data type of last_name to VARCHAR(255)
ALTER TABLE dim_users
ALTER COLUMN last_name TYPE VARCHAR(255);

-- Change data type of date_of_birth to DATE
ALTER TABLE dim_users
ALTER COLUMN date_of_birth TYPE DATE;

-- Change data type of country_code to VARCHAR(4)
ALTER TABLE dim_users
ALTER COLUMN country_code TYPE VARCHAR(4);

-- Change data type of user_uuid to UUID
ALTER TABLE dim_users
ALTER COLUMN user_uuid TYPE UUID
USING user_uuid::UUID;

-- Change data type of join_date to DATE
ALTER TABLE dim_users
ALTER COLUMN join_date TYPE DATE;

-- Set Primary key constraint
ALTER TABLE dim_users
ADD PRIMARY KEY (user_uuid);