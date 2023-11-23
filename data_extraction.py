from database_utils import DatabaseConnector

class DataExtractor:
    """
    This class will work as a utility class and contain methods that help extract data 
    from different data sources like an RDS, CSV files, an API or an S3 bucket
    """
    def read_rds_table(self, db_connector:DatabaseConnector, table_name:str):
        """
        Extract the RDS database table to a pandas DataFrame

        Takes an instance of the DatabaseConnector class and a table name as an argument
        and extracts the table containing user data to a pandas DataFrame.

        Parameters:
        ----------
        db_connector: DatabaseConnector
            Instance of the DatabaseConnector class used to connect to the AWS RDS DB and list tables within it

        table_name: string
            Name of the table to extract data from

        Returns:
        -------
        <class 'pandas.core.frame.DataFrame'>
            DataFrame containing data from 'table_name'
        """
        import pandas as pd
        return pd.read_sql_table(table_name, db_connector.engine)
    
    def retrieve_pdf_data(self, pdf_path:str):
        """
        This method extracts data from a PDF link and returns a pandas DataFrame

        Parameters:
        ----------
        pdf_path: string
            The link to PDF to extract data from

        Returns:
        -------
        list of <class 'pandas.core.frame.DataFrame'>
            DataFrame containing data extracted from PDF at the link
        """
        import tabula

        return tabula.read_pdf(pdf_path, pages='all')
    
    def __read_api_creds(self, creds_file_name):
        """
        Read api_creds.yaml file containing the api key

        Parameters: 
        ----------
        creds_file_name: string
            Filename of the file to read DB Credentials from

        Returns:
        --------
        <class 'dict'>
            A dictionary containing credentials read from db_creds.yaml
        """
        import yaml
        with open(creds_file_name, 'r') as file:
            return yaml.safe_load(file)
    
    def list_number_of_stores(self, stores_count_url:str):
        """
        Method to get the total number of stores
        """
        import requests
        header_details = self.__read_api_creds('api_creds.yaml')
        r = requests.get(stores_count_url, headers=header_details)
        return r.json()['number_stores']
    
    def retrieve_store_data(self, store_by_number_url:str):
        """
        Method to retrieve store details for the given store number
        """
        import requests
        header_details = self.__read_api_creds('api_creds.yaml')
        return requests.get(store_by_number_url, headers=header_details)
    
    def get_stores(self):
        """
        Method to fetch the number of stores and then get the data for each store
        The data is collected in a list and then returned as a DataFrame
        """
        import json
        import pandas as pd
        
        store_by_number_url = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}"
        stores_count_url = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
        
        num_stores = self.list_number_of_stores(stores_count_url)

        stores = []

        for i in range(0, num_stores):  
            response = self.retrieve_store_data(store_by_number_url.replace('{store_number}', str(i)))

            if response.status_code == 200:
                stores.append(json.loads(response.content.decode()))
            else:
                print(f"Error for request {i}: {response.status_code}")
        
        return pd.json_normalize(stores)
    
    def extract_from_s3(self):
        """
        Method to extract data from a CSV in an S3 bucket
        into a DataFrame and return it
        """
        import pandas as pd
        import boto3
        from io import BytesIO

        bucket_name = 'data-handling-public'
        file_key = 'products.csv'

        # Create an S3 client
        s3 = boto3.client('s3')

        # Read the CSV file into a Pandas DataFrame
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        df = pd.read_csv(BytesIO(obj['Body'].read()), index_col=0, header=0)
        print(f"{file_key}: data loaded successfully")

        return df

    

if __name__ == "__main__":
    dbe = DataExtractor()
    # dbc = DatabaseConnector('db_creds.yaml')
    # df = dbe.read_rds_table(dbc, 'legacy_users')
    # print(df.head())

    # link_to_pdf = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
    # print(dbe.retrieve_pdf_data(link_to_pdf))

    df = dbe.get_stores()
    print(df.head())