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

-- Drop the tables if they exist
DROP TABLE IF EXISTS Matches CASCADE;
DROP TABLE IF EXISTS MatchInfo CASCADE;

-- Matches
CREATE TABLE IF NOT EXISTS Matches (
    match_id INTEGER PRIMARY KEY,
    home_team_name VARCHAR(255),
    away_team_name VARCHAR(255),
    home_team_goals INTEGER,
    away_team_goals INTEGER

);

-- Matchinfo
CREATE TABLE IF NOT EXISTS MatchInfo (
    match_id INTEGER REFERENCES Matches(match_id),
    shirt_number INTEGER,
    club_name VARCHAR(255),
    goals_scored INTEGER
);

-- Insert sample data into the Matches table
INSERT INTO Matches (match_id , home_team_name, away_team_name , home_team_goals , away_team_goals)
VALUES 
    ('0','Home Team A','Away Team X','3','1');
   
-- Insert sample data into the MatchInfo table
INSERT INTO MatchInfo (match_id, shirt_number, club_name, goals_scored)
VALUES 
    (0, 10,'Home Team A', 2);
   






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
