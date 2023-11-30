from data_cleaning import DataCleaning
from database_utils import DatabaseConnector

def get_db_tables_from_aws_rds():
    """
    Function to use the DatabaseConnector to connect to the RDS instance on AWS 
    and fetch the list of tables in it
    """
    dbconn = DatabaseConnector('db_creds.yaml')
    print(dbconn.list_db_tables())


def upload_tables_to_local_db(table_name:str, db_connector:DatabaseConnector, data_cleaning:DataCleaning):
    """
    Method used to extract data from various sources, clean it and then upload it
    to corresponding tables in the local instance of Postgres DB

    Parameters:
    ----------
    table_name: str
        Name of the table to which the cleaned data is uploaded

    db_connector: DatabaseConnector
        Instance of DatabaseConnector to connect to the local DB

    data_cleaning: DataCleaning
        Instance of the DataCleaning class to call the cleaning methods 
        corresponding to each data source
    """

    match table_name:
        case 'dim_users':
            df_users = data_cleaning.clean_user_data()
            db_connector.upload_to_db(df_users, 'dim_users')

        case 'dim_card_details':
            df_cards = data_cleaning.clean_card_data()
            db_connector.upload_to_db(df_cards, 'dim_card_details')

        case 'dim_store_details':
            df_stores = data_cleaning.clean_store_data()
            db_connector.upload_to_db(df_stores, 'dim_store_details')

        case 'dim_products':
            df_products = data_cleaning.clean_products_data()
            db_connector.upload_to_db(df_products, 'dim_products')

        case 'orders_table':
            df_orders = data_cleaning.clean_orders_data()
            db_connector.upload_to_db(df_orders, 'orders_table')

        case 'dim_date_times':
            df_timedetails = data_cleaning.clean_time_detail()
            db_connector.upload_to_db(df_timedetails, 'dim_date_times')

if __name__ == "__main__":
    
    data_cleaning = DataCleaning()
    db_conn_local = DatabaseConnector('db_creds_local.yaml')

    upload_tables_to_local_db('dim_users', db_conn_local, data_cleaning)
    upload_tables_to_local_db('dim_card_details', db_conn_local, data_cleaning)
    upload_tables_to_local_db('dim_store_details', db_conn_local, data_cleaning)
    upload_tables_to_local_db('dim_products', db_conn_local, data_cleaning)
    upload_tables_to_local_db('orders_table', db_conn_local, data_cleaning)
    upload_tables_to_local_db('dim_date_times', db_conn_local, data_cleaning)

