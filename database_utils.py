class DatabaseConnector:
    """
    Class to connect to database
    """
    def read_db_creds(self):
        """
        Read db_creds.yaml file containing the database credentials and return a dictionary of the credentials

        Returns:
        --------
        <class 'dict'>
            A dictionary containing credentials read from db_creds.yaml
        """
        import yaml
        with open('db_creds.yaml', 'r') as file:
            return yaml.safe_load(file)
        

    def init_db_engine(self):
        """
        Read database credentials from the credentials file and initialise and return a sqlalchemy database engine
        
        Returns:
        --------
        <class 'sqlalchemy.engine.base.Engine'>
            Initialised instance of the SQLAlchemy Database Engine object
        """
        db_creds = self.read_db_creds()

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
        engine = self.init_db_engine()
        engine.connect()

        from sqlalchemy import inspect
        inspector = inspect(engine)
        return inspector.get_table_names()

if __name__ == "__main__":
    dbc = DatabaseConnector()
    print(dbc.list_db_tables())