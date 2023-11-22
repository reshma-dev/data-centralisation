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

if __name__ == "__main__":
    dbe = DataExtractor()
    # dbc = DatabaseConnector('db_creds.yaml')
    # df = dbe.read_rds_table(dbc, 'legacy_users')
    # print(df.head())

    link_to_pdf = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
    print(dbe.retrieve_pdf_data(link_to_pdf))