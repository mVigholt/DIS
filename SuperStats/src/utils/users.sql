DROP TABLE IF EXISTS Users CASCADE;

CREATE TABLE IF NOT EXISTS Users(
	pk serial not null PRIMARY KEY,
	user_name varchar(50) UNIQUE,
    full_name varchar(50),
	password varchar(120),
    club_name varchar(50)
);

CREATE INDEX IF NOT EXISTS users_index
ON Users (pk, user_name);

DELETE FROM Users;


-- Drop the Users table if it exists, along with any dependent objects
DROP TABLE IF EXISTS Managers CASCADE;

-- Create the Managers table with the required fields
CREATE TABLE IF NOT EXISTS Managers(
    PRIMARY KEY(pk)
) INHERITS (Users);

-- Create an index on the Managers table
CREATE INDEX IF NOT EXISTS managers_index
ON Managers (pk, user_name);

-- Delete all records from the Managers table
DELETE FROM Managers;

-- Insert a sample manager into the Managers table
INSERT INTO Managers(user_name,full_name, password, club_name)
VALUES ('Thomas','Sample Manager', 'pass', 'Sample Club');

DROP TABLE IF EXISTS Farmers CASCADE;

CREATE TABLE IF NOT EXISTS Farmers(
    PRIMARY KEY(pk)
) INHERITS (Users);

CREATE INDEX IF NOT EXISTS farmers_index
ON Farmers (pk, user_name);

DELETE FROM Farmers;

INSERT INTO Farmers(user_name, full_name, password, club_name)
VALUES ('farmer', 'Farmer', 'pass', 'Farmer Club');

DROP TABLE IF EXISTS Customers;

CREATE TABLE IF NOT EXISTS Customers(
    PRIMARY KEY(pk)
) INHERITS (Users);

CREATE INDEX IF NOT EXISTS customers_index
ON Customers (pk, user_name);

DELETE FROM Customers;

INSERT INTO Customers(user_name, full_name, password, club_name)
VALUES ('customer', 'Customer', 'pass', 'Customer Club');
