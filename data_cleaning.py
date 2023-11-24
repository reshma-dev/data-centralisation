class DataCleaning():
    """
    A utility class with methods to clean data from each of the data sources
    """
    
    def is_within_int32_range(self, column_name, df):
        """
        Method to check if all the values in the column 'column_name', 
        are within the int32 range

        Parameters:
        ----------
        column_name: string
            Column name of the column whose values are to be checked

        df: <class 'pandas.core.frame.DataFrame'>
            The DataFrame to which the column belongs

        Returns:
        --------
        True if all the values in column_name are within int32 range
        False if one or more values are out of range

        """
        import numpy as np

        # Get the minimum and maximum values of the column
        min_value = df[column_name].min()
        max_value = df[column_name].max()

        # Check if both min and max values are within the int32 range
        return np.int32(min_value) >= np.iinfo(np.int32).min and np.int32(max_value) <= np.iinfo(np.int32).max
    
    
    def clean_user_data(self):
        """
        Method for cleaning of the legacy_users data 
        Look for NULL values, errors with dates, incorrectly typed values and rows filled with the wrong information
        """
        import pandas as pd
        from data_extraction import DataExtractor
        from database_utils import DatabaseConnector

        dbe = DataExtractor()
        dbc = DatabaseConnector('db_creds.yaml')

        # Read contents of the legacy_users table
        df = dbe.read_rds_table(dbc, 'legacy_users')
        print(f"Number of records in the 'legacy_users' table: {len(df)}")
        # 1. Set correct data types to the columns of the DataFrame

        # Index range for this table is 0 to 15319, but to avoid overflow errors if used on another table, 
        # check all values are within int32 range and convert type from 64 to 32 to save memory
        if self.is_within_int32_range('index', df):
            df['index'] = df['index'].astype('int32')

        # Convert text columns from `object` to `string`
        # - useful to be able to perform string operations
        # - string dtype is also more memory-efficient
        df.first_name = df.first_name.astype('string')
        df.last_name = df.last_name.astype('string')
        df.company = df.company.astype('string')
        df.email_address = df.email_address.astype('string')
        df.address = df.address.astype('string')
        df.phone_number = df.phone_number.astype('string')
        df.user_uuid = df.user_uuid.astype('string')

        # Convert country and country_code to `category`
        df.country = df.country.astype('category')
        df.country_code = df.country_code.astype('category')

        # Convert date fields to date
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], format='mixed', errors='coerce')

        num_errors = df['date_of_birth'].isna().sum()
        print(f"Number of records with invalid date_of_birth: {num_errors}")

        # Convert remaining date column to date type
        df['join_date'] = pd.to_datetime(df['join_date'], format='mixed', errors='coerce')

        # 2. Drop all rows where the DOB and all other entries were invalid (36 rows dropped)
        df = df.dropna(subset=['date_of_birth'])
        print(f"Records with invalid DOB had other entries invalid too. Number of records after dropping invalid rows: {len(df)}")

        # 3. Check for duplicate entries
        df = df.drop_duplicates(subset='user_uuid', keep='first')
        print(f"Number of records after removing duplicates: {len(df)}")

        # 4. Validate that the join_date is after the date_of_birth
        # Calculate the time difference between 'join_date' and 'date_of_birth'
        time_difference = df['join_date'] - df['date_of_birth']

        # As columns other than the DOJ seem to have valid data, we don't drop all rows with negative difference, 
        # just add a new column 'invalid_date_flag' to flag invalid entries
        df['invalid_date_flag'] = time_difference < pd.Timedelta(0)

        # Display the rows with invalid entries
        print(f"Number of entries with invalid dates: {df['invalid_date_flag'].sum()}")
        return df

    def clean_card_data(self):
        """
        Method for cleaning card data extracted from a PDF
        """
        from data_extraction import DataExtractor
        dbe = DataExtractor()
        link_to_pdf = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
        
        df_list = dbe.retrieve_pdf_data(link_to_pdf)
        
        import pandas as pd
        df = pd.concat(df_list, ignore_index=True)

        # 1. Set data types
        df.card_number = df.card_number.astype('string')
        df.expiry_date = df.expiry_date.astype('string')
        df.card_provider = df.card_provider.astype('category')

        # 2. Eliminate invalid rows using expiry date column 

        # Add a new column to look at which 'expiry_date' entries fail to parse to MM/YY format
        df['invalid_exp_date'] = pd.to_datetime(df.expiry_date, format='%m/%y', errors='coerce')
        print(f"Number of rows with invalid expiry date: {len(df[df['invalid_exp_date'].isna()])}")

        # As all other columns in the filtered set contain invalid data too,
        # it's safe to drop all rows where the expiry_date is invalid (25 rows dropped)
        # i.e. where invalid_exp_date is NaT
        df = df.dropna(subset=['invalid_exp_date'])

        # Delete the temporary column from data frame
        df = df.drop(['invalid_exp_date'], axis=1)

        # 3. Set Data type of the date_payment_confirmed column to datetime
        df['date_payment_confirmed'] = pd.to_datetime(df.date_payment_confirmed, format='mixed', errors='coerce') 
        print("No payment date entries failed to parse")

        # 4. Check for duplicate card_number entries
        df = df.drop_duplicates(subset='card_number', keep='first')
        print("No duplicate card_numbers were found")
        
        # 5. Remove non-digit characters from card_number
        df['card_number'] = df['card_number'].str.replace(r'[^0-9]?', '', regex=True)

        return df
    
    def clean_store_data(self):
        """
        Method for cleaning store data retrieved using an API
        """
        import pandas as pd
        import numpy as np

        from data_extraction import DataExtractor
        dbe = DataExtractor()
        df = dbe.get_stores()

        # 1. Delete the 'lat' column as it does not seem to contain any valid entries
        
        # Column 'lat' contains only 11 non-null objects
        # Check what the non-nulls are, to know if it is ok to delete the column
        # df[~df.lat.isna()]
        
        df = df.drop(['lat'], axis=1)

        # 2. Delete rows containing all NULL strings as values. These rows don't get caught in dropna, so first
        #    replace 'NULL' string with NaN to be able to delete them using dropna
        df.replace('NULL', np.nan, inplace=True)

        # 'thresh' specifies the minimum number of non-null values required for a row to be retained
        #  we want to retain all rows where even a single column (along with non-NaN index) is non-NaN, so set to '2'
        df.dropna(thresh=2, inplace=True)

        # 3. Set data types
        # if self.is_within_int32_range('index', df):
        df['index'] = df['index'].astype('int32')

        # string columns
        df.address = df.address.astype('string')
        df.locality = df.locality.astype('string')
        df.store_code = df.store_code.astype('string')

        # Rows with invalid opening date contain all other values invalid too, so delete those rows
        df['opening_dt_tmp'] = pd.to_datetime(df.opening_date, format='mixed', errors='coerce')
        df = df.dropna(subset=['opening_dt_tmp'])

        # Delete the temp column
        df = df.drop('opening_dt_tmp', axis=1)

        # Set latitude and longitude to float
        # Replace 'N/A' with pd.NA
        df['longitude'].replace('N/A', pd.NA, inplace=True)
        df['latitude'].replace('N/A', pd.NA, inplace=True)

        # Convert the column to numeric, handling pd.NA
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')

        df['longitude'] = df['longitude'].astype(float)
        df['latitude'] = df['latitude'].astype(float)

        # category columns
        df.store_type = df.store_type.astype('category')
        df.country_code = df.country_code.astype('category')
        df.continent = df.continent.astype('category')

        # numeric
        df['staff_numbers_tmp'] = pd.to_numeric(df['staff_numbers'], errors='coerce')
        df[df['staff_numbers_tmp'].isna()]

        # 4. Fix typos in the staff_numbers column
        # As rows where staff_numbers column contains alphabets contain valid data in rest of the columns
        # those alphas look like typos, so remove the alphabets to keep only numberic data
        df['staff_numbers'] = df['staff_numbers'].str.replace(r'[^0-9]?', '', regex=True)
        # then convert dtype to numeric
        df.staff_numbers = df.staff_numbers.astype('int32')

        # delete temp column
        df.drop(['staff_numbers_tmp'], axis=1)

        # 5. Fix typos in continent column
        df.continent.unique()
        df.continent = df.continent.replace('eeAmerica', 'America')
        df.continent = df.continent.replace('eeEurope', 'Europe')
        return df
    
    def convert_product_weights(self, products_df):
        """
        Method to convert varying units to equivalent kg
        """
        import pandas as pd
        
        # Define a function to convert different units to kg
        def convert_to_kg(weight_str):
            
            import re
            # Extract numerical values and unit from the weight string
            # Looking for digits followed by optional 'x' and more digits followed by unit as 3 groups
            match = re.match(r'([\d.]+)\s*x?\s*([\d.]+)?\s*([\w]+)', weight_str)
            
            if match:
                value1, value2, unit = match.groups()
                value1 = float(value1)
                
                # If 'x' is present, calculate the product of the two values
                if value2:
                    value2 = float(value2)
                    value = value1 * value2
                else:
                    value = value1
                
                # Convert to kg based on unit
                if unit == 'kg':
                    return value
                elif unit == 'g':
                    return value / 1000
                elif unit == 'oz':
                    return value * 0.0283495  # 1 oz is approximately 0.0283495 kg
                elif unit == 'ml':
                    return value / 1000  # 1 ml is approximately 1 g
                else:
                    return value  # Return value for unsupported units
            else:
                return None  # Return None if the format is not recognized

        # Apply the conversion function to the 'weight' column
        products_df['weight'] = products_df['weight'].apply(lambda x: convert_to_kg(x) if pd.notna(x) else x)
        
        return products_df
 
    def clean_products_data(self):
        """
        Method to clean products data
        """
        import pandas as pd

        from data_extraction import DataExtractor
        dbe = DataExtractor()

        bucket_name = 'data-handling-public'
        file_key = 'products.csv'

        df = dbe.extract_from_s3(bucket_name=bucket_name, file_key=file_key)

        # 1. Drop the rows containing all columns with 'NULL'
        df = df.dropna()

        # 2. Set string and category dtypes
        df.product_name = df.product_name.astype('string')
        df.product_price = df.product_price.astype('string')
        df.category = df.category.astype('category')
        df.EAN = df.EAN.astype('string')
        df.uuid = df.uuid.astype('string')
        df.removed = df.removed.astype('category')
        df.product_code = df.product_code.astype('string')

        # 3. Set date type & eliminate invalid rows
        df['date_added'] = pd.to_datetime(df['date_added'], format='mixed', errors='coerce')
        df = df.dropna(subset = ['date_added'])

        # 4. Convert weights to kg
        df = self.convert_product_weights(df)

        return df

    def clean_orders_data(self):
        """
        Method for cleaning orders data
        """
        from data_extraction import DataExtractor
        from database_utils import DatabaseConnector

        dbe = DataExtractor()
        dbc = DatabaseConnector('db_creds.yaml')

        # Read contents of the orders_table table
        df = dbe.read_rds_table(dbc, 'orders_table')

        # Drop the invalid columns
        df = df.drop(['1', 'first_name', 'last_name'], axis=1)

        # Set data types
        df.date_uuid = df.date_uuid.astype('string')
        df.user_uuid = df.user_uuid.astype('string')
        df.card_number = df.card_number.astype('string')
        df.store_code = df.store_code.astype('string')
        df.product_code = df.product_code.astype('string')
        
        return df
    
    def clean_time_detail(self):
        """
        Method to clean time detail data
        """
        import pandas as pd

        from data_extraction import DataExtractor
        dbe = DataExtractor()

        bucket_name = 'data-handling-public'
        file_key = 'date_details.json'

        df = dbe.extract_from_s3(bucket_name=bucket_name, file_key=file_key)

        # 1. Drop the rows containing 'NULL' or invalid entries using timestamp
        df['timestamp_temp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')
        df = df.dropna(subset=['timestamp_temp'])
        df = df.drop(['timestamp_temp'], axis=1)
        
        # 2. Set dtypes
        df.time_period = df.time_period.astype('category')
        df.date_uuid = df.date_uuid.astype('string')

        df.month = df.month.astype('int16')
        df.year = df.year.astype('int16')
        df.day = df.day.astype('int16')

        return df

if __name__ == "__main__":
    dc = DataCleaning()
    # user_data = dc.clean_user_data()
    # print("Records with invalid join dates: \n", user_data[user_data['invalid_date_flag']])

    # cleaned_card_data = dc.clean_card_data()
    # print(f"Number of cleaned rows: {len(cleaned_card_data)}")
    # print(cleaned_card_data.head(20))

    # store_data = dc.clean_store_data()
    # print(store_data.info())
    # print(store_data.tail(25))

    # prod_data = dc.clean_products_data()
    # print(prod_data.info())
    # print(prod_data.tail())

    # orders_data = dc.clean_orders_data()
    # print(orders_data.info())
    # print(orders_data.tail())

    time_data = dc.clean_time_detail()
    print(time_data.info())
    print(time_data.tail())