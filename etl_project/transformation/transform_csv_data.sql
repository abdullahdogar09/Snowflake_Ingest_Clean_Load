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
-- Adding a labelling column on Company Size column 
ALTER TABLE my_table ADD COLUMN COMPANY_SIZE_LABELS STRING;

UPDATE my_table
SET COMPANY_SIZE_LABELS = CASE
    WHEN COMPANY_SIZE BETWEEN 1 AND 3 THEN 'micro-company'
    WHEN COMPANY_SIZE BETWEEN 4 AND 6 THEN 'mini-company'
    WHEN COMPANY_SIZE >= 7 THEN 'small-company'
    ELSE 'unknown'
END;

-- count total rows in the table (24473)
SELECT COUNT(*) FROM my_table;

------------------------------------------------------------------------------------------------------------------------------------------------
-- Dropping the very last row of the table 
DELETE FROM my_table
WHERE ID = (SELECT MAX(ID) FROM my_table);

------------------------------------------------------------------------------------------------------------------------------------------------
-- Deleting rows where STATE = 0 (2174)
DELETE FROM my_table
WHERE STATE = '0';

------------------------------------------------------------------------------------------------------------------------------------------------
--  Querying table in descending order 
SELECT * FROM my_table ORDER BY ID DESC LIMIT 50;
-- You cannot alter table in ascending/descending order because of columnar storage (snowflake will later rearrange rows)

------------------------------------------------------------------------------------------------------------------------------------------------