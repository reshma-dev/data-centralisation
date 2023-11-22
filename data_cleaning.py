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

if __name__ == "__main__":
    dc = DataCleaning()
    user_data = dc.clean_user_data()
    print("Records with invalid join dates: \n", user_data[user_data['invalid_date_flag']])