# Data Centralisation

### Table of Contents
**[Introduction](#introduction)**<br>
**[Installation Instructions](#installation-instructions)**<br>
**[Usage Instructions](#usage-instructions)**<br>
**[File structure of the project](#file-structure-of-the-project)**<br>
**[Lessons learnt](#lessons-learnt)**<br>

## Introduction

This project focuses on data ingestion, cleaning and then querying for analysing to find meaningful trends. It uses data of a multinational retail company where the data sources are spread across different locations and come in different formats. For example CSV, PDF or JSON files from an S3 bucket or from an RDS instance in AWS or via API.

Data from all these sources is extracted and cleaned using Python and the Pandas library and then uploaded to a local PostgreSQL instance. Once within the RDS, set data types for columns in all the tables to help with the Analysis later, create the database schema and possibly some more minor data cleaning tasks. 

Data Analysis is then done within the Relational Database using SQL.

## Installation Instructions

Following tools and libraries have been used in this project.  
Conda environment export is available in `data-central-env.yml` [here](/data-central-env.yml)

### Python 3.11
    - pandas                    2.1.1
    - boto3                     1.29.1
    - sqlalchemy                2.0.21
    - numpy                     1.26.0
    - requests                  2.31.0
    - tabula-py                 2.6.0
    - yaml                      0.2.5

### pgAdmin4

## Usage Instructions
- The code expects 3 credentials files with the names below, in the root directory of the project:
    - db_creds.yaml: File to hold the credentials to connect to the RDS instance in AWS for extracting the users data
    Expected fields:
        ```
        RDS_HOST: <AWS RDS instance>.rds.amazonaws.com
        RDS_PASSWORD: 
        RDS_USER: 
        RDS_DATABASE: 
        RDS_PORT: 
        ```
    - api_creds.yaml: API key to access the stores data
    Expected fields:
        ```
        x-api-key:
        ```
    - db_creds_local.yaml: Credentials to connect to the local PostgreSQL instance where the cleaned data is uploaded for analysis
    Expected fields:
        ```
        RDS_HOST: <PostgreSQL Instance to upload data to>
        RDS_PASSWORD: 
        RDS_USER: 
        RDS_DATABASE: 
        RDS_PORT: 
        ```

- Run `process_and_upload.py`: This file contains calls to extract data from all the sources and upload it into the PostgreSQL instance for analysis

- Use pgAdmin to execute queries for analysing data. The queries can be found under the `sql/analysis_queries` folder

## File structure of the project

### The Python codebase is divided into three parts:
- Data Extraction
    Contains `DataExtractor` as a utility class with methods that help extract data from different data sources.
    The methods correspond to each data source like CSV files from an S3 bucket, an API or an RDS instance on AWS.
- Data Cleaning
    Contains `DataCleaning` class with methods to clean data from each of the data sources
- Utilities
    Contains `DatabaseConnector` class for connecting to and accessing or uploading data

### SQL scripts in the `sql` folder are of two categories:
- `update_*.sql` scripts per table for setting column types and any clean-up tasks that might be needed after data is imported into the DB and building relationships between the tables
- `taskx_*.sql` scripts with queries for analysing the data

### Star schema created for the project:
![Star-schema-retail-data](/images/star-schema-retail-data.png)

## Lessons learnt

- Exploring data in notebooks made data cleaning easier and faster. Created `explore_*.ipynb` file per table so it's still available for debugging or reminding of decisions during the transformation process. Once happy, made them into functions to transfer to the scripts for the data flow pipeline.

- Steps followed for the cleaning phase:

    1. Set appropriate data types to the Dataframe columns: This helped get rid of rows with invalid data very quickly and easily. For example, the text snippets in date fields that did not parse with `to_datetime()` helped spot that the entire row was full of invalid data so was safe to delete
    
        For example, for products data:
        ```
        # 3. Set date type & eliminate invalid rows
        
        df['date_added'] = pd.to_datetime(df['date_added'], format='mixed', errors='coerce')
        
        df = df.dropna(subset = ['date_added'])
        ```
        During the exploration phase, it was useful to create a temporary column with the new data type or change so that the original and new could be compared side-by-side and once happy, the script could make the change to the original column.

        For example, to clean the alphabet occurances from the staff number column
        ```
        # Create a new column `staff_numbers_tmp` with data type numeric
        
        df['staff_numbers_tmp'] = pd.to_numeric(df['staff_numbers'], errors='coerce')
        df[df['staff_numbers_tmp'].isna()]

        # As rows where staff_numbers column contains alphabets contain valid data in rest of the columns
        # those alphas look like typos, so remove the alphabets to keep only numberic data
        
        df['staff_numbers'] = df['staff_numbers'].str.replace(r'[^0-9]?', '', regex=True)
        
        # then convert dtype to numeric
        df.staff_numbers = df.staff_numbers.astype('int32')

        # delete temp column
        df = df.drop(['staff_numbers_tmp'], axis=1)
        ```
    2. Check for NaN or NULL values and duplicated data

    3. Any data discrepancies spotted during the cleaning phase that were not clearly or confidently incorrect were marked in a new column so that during the Analysis phase, the queries would still see the data if needed, as well as have a handy extra column for making it easy to spot the discrepancies. For example, in some cases, the Date of joining was before Date of birth, but all other columns had correct-looking data, so added a new column `invalid_date_flag` to mark such cases.