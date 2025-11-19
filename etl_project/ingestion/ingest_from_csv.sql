-------------------------------------------------------------------------------------------------------------------------------------------
-- USER INTERFACE METHOD TO LOAD DATA INTO A TABLE FROM CSV IN SSTAGE
-- To work in Snowflake, you first need a database
CREATE OR REPLACE DATABASE csv_data;

-- The second thing is to create a schema inside your database
CREATE OR REPLACE SCHEMA raw_data;

-- List all schemas in a database 
SHOW SCHEMAS;

-- I forgot to create a warehouse
CREATE OR REPLACE WAREHOUSE ingest_wh;
USE WAREHOUSE ingest_wh;

-- Use a specific Database
USE DATABASE csv_data;
USE SCHEMA raw_data;

-- Create an internal stage to load the CSV file into it 
CREATE OR REPLACE STAGE csv;
LIST @csv;

-- Check the column names in the table 
DESC TABLE RAW_TABLE;

-- Truncate table or Drop Table
TRUNCATE TABLE RAW_TABLE;
DROP TABLE RAW_TABLE;

SHOW TABLES;
---------------------------------------------------------------------------------------------------------------------------------------------
-- MANUAL SQL METHOD TO LOAD DATA INTO A TABLE FROM CSV IN STAGE
-- Creating a file format
CREATE OR REPLACE FILE FORMAT my_csv_format
TYPE = 'CSV'
FIELD_DELIMITER = ','
PARSE_HEADER = TRUE
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
TRIM_SPACE = TRUE;

-- List all the available File Formats
SHOW FILE FORMATS;

-- Dropping a file format
DROP FILE FORMAT my_csv_format;

-- Creating a new table Structure from a staging csv file
CREATE OR REPLACE TABLE my_table
USING TEMPLATE(
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@csv/',
            FILE_FORMAT => 'my_csv_format'
        )
    )
);

-- Inserting Data into the new table 
COPY INTO my_table
FROM @csv/
FILE_FORMAT = (FORMAT_NAME = 'my_csv_format')
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'CONTINUE';

-- Describe new Table
DESC TABLE my_table;

SELECT * FROM my_table;

-- Drop Table
DROP TABLE MY_TABLE;


