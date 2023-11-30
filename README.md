# Data Centralisation

### Table of Contents
**[Introduction](#introduction)**<br>
**[Installation Instructions](#installation-instructions)**<br>
**[Usage Instructions](#usage-instructions)**<br>
**[File structure of the project](#file-structure-of-the-project)**<br>

## Introduction

This project focuses on data ingestion, cleaning and then querying for analysing to find meaningful trends. It uses data of a multinational retail company where the data sources are spread across different locations and come in different formats. For example CSV, PDF or JSON files from an S3 bucket or from an RDS instance in AWS or via API.

Data from all these sources is extracted and cleaned using Python and the Pandas library and then uploaded to a local PostgreSQL instance. Once within the RDS, set data types for columns in all the tables to help with the Analysis later, create the database schema and possibly some more minor data cleaning tasks. 

Data Analysis is then done within the Relational Database using SQL.

## Installation Instructions

Following tools and libraries have been used in this project

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

- Use pgAdmin to execute queries for analysing data. The queries can be found under the `sql` folder

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