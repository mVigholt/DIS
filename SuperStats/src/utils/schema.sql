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

DROP TABLE IF EXISTS Players CASCADE;

CREATE TABLE IF NOT EXISTS  Players(
    shirt_number int not null,
    club_name varchar(100),
    player_name varchar(100),
    nationality varchar(100),
    goals int,
    PRIMARY KEY (shirt_number, club_name)
);

DELETE FROM Players;

CREATE INDEX IF NOT EXISTS players_index
ON Players (shirt_number, club_name);


DROP TABLE IF EXISTS Clubs CASCADE;

CREATE TABLE IF NOT EXISTS Clubs(
    club_name varchar(100) not null PRIMARY KEY,
    manager_name varchar(100),
    games_played int,
    wins int,
    draws int,
    losses int,
    points int,
    goals_scored int,
    goals_conceded int,
    goal_difference int
);

DELETE FROM Clubs;

CREATE INDEX IF NOT EXISTS clubs_index
ON Clubs (club_name);


-- Insert sample data into the Matches table
INSERT INTO Matches (match_id , home_team_name, away_team_name , home_team_goals , away_team_goals)
VALUES ('0','Home Team A','Away Team X','3','1');
   
-- Insert sample data into the MatchInfo table
INSERT INTO MatchInfo (match_id, shirt_number, club_name, goals_scored)
VALUES (0, 10,'Home Team A', 2);

-- Insert a sample manager into the Managers table
INSERT INTO Managers(user_name,full_name, password, club_name)
VALUES ('Thomas','Sample Manager', 'pass', 'Sample Club');
