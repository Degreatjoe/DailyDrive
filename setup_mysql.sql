-- Prepare a MySQL server for the project

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS DD_dev_db;

-- Create the user if it doesn't exist
CREATE USER IF NOT EXISTS 'DD_dev'@'localhost' IDENTIFIED BY 'Great#7729';

-- Grant all privileges on DD_dev_db to DD_dev
GRANT ALL PRIVILEGES ON DD_dev_db.* TO 'DD_dev'@'localhost';

-- Grant SELECT privilege on performance_schema to DD_dev
GRANT SELECT ON performance_schema.* TO 'DD_dev'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
