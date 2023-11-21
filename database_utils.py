class DatabaseConnector:
    """
    Class to connect to database
    """
    def read_db_creds(self, creds_file_name):
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
        

    def init_db_engine(self, creds_file_name):
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
        db_creds = self.read_db_creds(creds_file_name)

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
        Use init_db_engine() to connect to the database and list all the tables in the connected database

        Returns:
        --------
        list
            List of all the tables in the connected database
        """
        engine = self.init_db_engine('db_creds.yaml')

        with engine.execution_options(isolation_level='AUTOCOMMIT').connect() as conn:
            from sqlalchemy import inspect
            inspector = inspect(engine)
            return inspector.get_table_names()
        
    def upload_to_db(self, df, table_name):
        """
        This method will upload a Pandas DataFrame to a table.

        Parameter:
        df: <class 'pandas.core.frame.DataFrame'>
            The DataFrame from which data will be uploaded

        table_name: string
            The RDS table to which the data from DataFrame will be uploaded 
        """
        engine = self.init_db_engine('db_creds_local.yaml')

        with engine.execution_options(isolation_level='AUTOCOMMIT').connect() as conn:
            df.to_sql(table_name, conn, if_exists= 'replace')


if __name__ == "__main__":
    dbconn = DatabaseConnector()
    print(dbconn.list_db_tables())

    from data_cleaning import DataCleaning

    dbclean = DataCleaning()
    df = dbclean.clean_user_data()
    print(f"Number of clean entries: {len(df)}")

    dbconn.upload_to_db(df, 'dim_users')