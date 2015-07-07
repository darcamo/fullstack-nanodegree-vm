-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- Create the database (we drop if first if it already exists)
-- DROP DATABASE tournament;
-- CREATE DATABASE tournament;

-- Create the "players" table
CREATE TABLE players (
        p_name TEXT,
        p_id SERIAL PRIMARY KEY);

-- Create the matches table
CREATE TABLE matches (
        winner INT REFERENCES players(p_id),
        loser INT REFERENCES players(p_id),
        match_num SERIAL PRIMARY KEY);

-- View for the player wins
-- Note that we use left join so that we get a count even for players that
-- didn't had any wins yet
CREATE VIEW player_wins AS
SELECT players.p_id, COUNT(matches.winner) AS  wins
FROM players
    LEFT JOIN matches
    ON (players.p_id=matches.winner)
GROUP BY players.p_id;

-- View for the player losses
-- Note that we use left join so that we get a count even for players that
-- didn't had any losses yet
CREATE VIEW player_losses AS
SELECT players.p_id, COUNT(matches.loser) AS losses
FROM players
    LEFT JOIN matches
    ON (players.p_id=matches.loser)
GROUP BY players.p_id;


-- Create a view for the player standings
CREATE VIEW player_standings AS 
SELECT players.p_id,
    players.p_name as Name,
    player_wins.wins,
    player_wins.wins+player_losses.losses as matches
FROM players
    JOIN player_wins
    ON players.p_id=player_wins.p_id
    JOIN player_losses
    ON players.p_id=player_losses.p_id
ORDER BY player_wins.wins DESC;
