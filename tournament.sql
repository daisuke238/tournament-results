-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- creates tournament database
CREATE DATABASE tournament;

-- connect to tournament database
\c tournament;

-- creates players table with id (automatically generated) and name fields
CREATE TABLE players (
    id serial PRIMARY KEY,
    name text
);

-- creates matches table with id (automatically generated), player1 and player2 id, and winner_id fields
-- foreign keys are set on player1, player2, winner_id to the players table id field
CREATE TABLE matches (
    id serial PRIMARY KEY,
    player1 integer REFERENCES players (id),
    player2 integer REFERENCES players (id),
    winner_id integer REFERENCES players (id)
);

-- creates view win_count which gets all players and whatever matches won by them
-- output list contains players with most wins on the top
CREATE VIEW win_count AS
SELECT players.id as id, players.name, count(winner_id) as wins
FROM players LEFT JOIN matches ON players.id = matches.winner_id 
GROUP BY players.id, players.name
ORDER BY wins DESC;

-- creates view match_count which:
-- 1. gets all matches played by combining player1 column with player2 column
-- 2. gets all players and matches up against the results of #1 above
CREATE VIEW match_count AS
SELECT players.id, players.name, count(player_id) as num_matches
FROM players LEFT JOIN (
      SELECT player1 as player_id FROM matches
      UNION ALL
      SELECT player2 as player_id FROM matches) AS all_matches
ON players.id = all_matches.player_id
GROUP BY players.id, players.name
ORDER BY players.id ASC;

-- creates view player_standings which combines the 2 other views above to show for each player:
-- how many matches were played
-- how many matches were won
CREATE VIEW player_standings AS
SELECT win_count.id, win_count.name, win_count.wins, match_count.num_matches as matches
FROM win_count, match_count
WHERE win_count.id = match_count.id
ORDER BY wins DESC;
