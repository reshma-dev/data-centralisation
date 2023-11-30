SELECT * FROM dim_date_times;

SELECT MAX(CHAR_LENGTH(time_period)) FROM dim_date_times;
-- 10

-- Update column data types
ALTER TABLE dim_date_times
ALTER COLUMN month TYPE VARCHAR(2);

ALTER TABLE dim_date_times
ALTER COLUMN year TYPE VARCHAR(4);

ALTER TABLE dim_date_times
ALTER COLUMN day TYPE VARCHAR(2);

ALTER TABLE dim_date_times
ALTER COLUMN time_period TYPE VARCHAR(16);

ALTER TABLE dim_date_times
ALTER COLUMN date_uuid TYPE UUID
Using date_uuid::UUID;

-- View column data types
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dim_date_times';

-- Set Primary key
ALTER TABLE dim_date_times
ADD PRIMARY KEY (date_uuid);