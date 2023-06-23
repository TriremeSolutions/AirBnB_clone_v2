--   Create Database hbnb_test_db.
--   User hbnb_test. Password hbnb_test_pwd in localhost.
--   Grants all privileges for hbnb_test on hbnb_test_db.
--   Grants SELECT privileges for hbnb_test on performance_schema.

CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost';
SET PASSWORD FOR 'hbnb_test'@'localhost' = 'hbnb_test_pwd';
USE hbnb_test_db;
GRANT ALL PRIVILEGES
    ON hbnb_test_db.*
    TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.*
    TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;