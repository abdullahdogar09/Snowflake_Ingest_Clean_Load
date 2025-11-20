--------------------------------------------------------------------------------------------------------------------------------------------
SHOW WAREHOUSES;
USE WAREHOUSE INGEST_WH;
USE DATABASE CSV_DATA;
USE SCHEMA RAW_DATA;

-------------------------------------------------------------------------------------------------------------------------------------------------
-- List all the available tables
SHOW TABLES;
-- Describe Table
DESC TABLE my_table;

-------------------------------------------------------------------------------------------------------------------------------------------------
-- Total number of rows in a Table
SELECT COUNT(*) FROM my_table;

-- Total number of columns in a table
SELECT COUNT(*) AS Column_Count
FROM information_schema.COLUMNS
WHERE table_schema = 'RAW_DATA'
AND table_name = 'MY_TABLE';

-------------------------------------------------------------------------------------------------------------------------------------------------
