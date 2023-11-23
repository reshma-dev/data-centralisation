class DatabaseConnector:
    """
    Class to connect to database
    """
    def __init__(self, creds_file_name) -> None:
        self.engine = self.__init_db_engine(creds_file_name)
        
    def __read_db_creds(self, creds_file_name):
        """
        Read db_creds.yaml file containing the database credentials and return a dictionary of the credentials

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
        

    def __init_db_engine(self, creds_file_name):
        """
        Read database credentials from the credentials file and initialise and return a sqlalchemy database engine
        
        Parameters: 
        ----------
        creds_file_name: string
            Filename of the file to read DB Credentials from

        Returns:
        --------
        <class 'sqlalchemy.engine.base.Engine'>
            Initialised instance of the SQLAlchemy Database Engine object
        """
        db_creds = self.__read_db_creds(creds_file_name)

        from sqlalchemy import create_engine

        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = db_creds['RDS_HOST']
        USER = db_creds['RDS_USER']
        PASSWORD = db_creds['RDS_PASSWORD']
        DATABASE = db_creds['RDS_DATABASE']
        PORT = db_creds['RDS_PORT']

        return create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

    def list_db_tables(self):
        """
        Gets a list of all the tables in the connected database

        Returns:
        --------
        list
            List of all the tables in the connected database
        """

        with self.engine.execution_options(isolation_level='AUTOCOMMIT').connect() as conn:
            from sqlalchemy import inspect
            inspector = inspect(self.engine)
            return inspector.get_table_names()
        
    def upload_to_db(self, df, table_name):
        """
        This method will upload a Pandas DataFrame 'df' to a table 'table_name'.

        Parameter:
        df: <class 'pandas.core.frame.DataFrame'>
            The DataFrame from which data will be uploaded

        table_name: string
            The RDS table to which the data from DataFrame will be uploaded 
        """

        with self.engine.execution_options(isolation_level='AUTOCOMMIT').connect() as conn:
            df.to_sql(table_name, conn, if_exists= 'replace', index=False)


if __name__ == "__main__":
    dbconn = DatabaseConnector('db_creds.yaml')
    print(dbconn.list_db_tables())

    from data_cleaning import DataCleaning

    dbclean = DataCleaning()
    # df = dbclean.clean_user_data()
    # print(f"Number of clean entries: {len(df)}")

    dbconn_local = DatabaseConnector('db_creds_local.yaml')
    # dbconn_local.upload_to_db(df, 'dim_users')

    # df_cards = dbclean.clean_card_data()
    # print(f"Number of clean entries: {len(df_cards)}")

    # dbconn_local.upload_to_db(df_cards, 'dim_card_details')

    # df_stores = dbclean.clean_store_data()
    # dbconn_local.upload_to_db(df_stores, 'dim_store_details')

    df_products = dbclean.clean_products_data()
    dbconn_local.upload_to_db(df_products, 'dim_products')