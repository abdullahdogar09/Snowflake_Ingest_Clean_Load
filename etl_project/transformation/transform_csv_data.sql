USE DATABASE CSV_DATA;
USE SCHEMA RAW_DATA;
SHOW TABLES;

---------------------------------------------------------------------------------------------------------------------------------------------
-- Rename all column names to lowercase (printing SQL queries)
SELECT
    ' ALTER TABLE ' || table_schema || '.' || table_name || ' RENAME COLUMN "' || column_name || '" TO "' || UPPER(column_name) || '";'
    AS rename_columns
FROM information_schema.columns
WHERE table_schema = 'RAW_DATA'
AND table_name = 'MY_TABLE';

-- From the results of the above query, you can use statements
ALTER TABLE RAW_DATA.MY_TABLE RENAME COLUMN "url" TO "URL";
ALTER TABLE RAW_DATA.MY_TABLE RENAME COLUMN "description" TO "DESCRIPTION";
ALTER TABLE RAW_DATA.MY_TABLE RENAME COLUMN "address" TO "ADDRESS";
ALTER TABLE RAW_DATA.MY_TABLE RENAME COLUMN "company_id" TO "COMPANY_ID";
ALTER TABLE RAW_DATA.MY_TABLE RENAME COLUMN "city" TO "CITY";
ALTER TABLE RAW_DATA.MY_TABLE RENAME COLUMN "state" TO "STATE";
ALTER TABLE RAW_DATA.MY_TABLE RENAME COLUMN "zip_code" TO "ZIP_CODE";
ALTER TABLE RAW_DATA.MY_TABLE RENAME COLUMN "name" TO "NAME";
ALTER TABLE RAW_DATA.MY_TABLE RENAME COLUMN "company_size" TO "COMPANY_SIZE";
ALTER TABLE RAW_DATA.MY_TABLE RENAME COLUMN "country" TO "COUNTRY";

-----------------------------------------------------------------------------------------------------------------------------------------------
-- creating sequence on a table (index alternative) because snowflake doesn't support index 
CREATE SEQUENCE seq_my_table START = 1 INCREMENT = 1;
ALTER TABLE my_table ADD COLUMN ID NUMBER;
UPDATE my_table SET id = seq_my_table.NEXTVAL;

SELECT * FROM my_table LIMIT 20;

-----------------------------------------------------------------------------------------------------------------------------------------------
