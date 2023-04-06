-- SQL scripting
-- Create a new table
CREATE TABLE IF NOT EXISTS users (id INT NOT NULL, email VARCHAR(255) UNIQUE NOT NULL, name VARCHAR(255));
