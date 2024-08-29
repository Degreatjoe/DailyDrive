-- Prepare a MySQL server for the project

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS DD_test_db;

-- Create the user if it doesn't exist
CREATE USER IF NOT EXISTS 'DD_test'@'localhost' IDENTIFIED BY 'Great#7729';

-- Grant all privileges on DD_dev_db to DD_dev
GRANT ALL PRIVILEGES ON DD_test_db.* TO 'DD_test'@'localhost';

-- Grant SELECT privilege on performance_schema to DD_dev
GRANT SELECT ON performance_schema.* TO 'DD_test'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
