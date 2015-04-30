#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    query = "DELETE FROM matches;"
    c.execute(query)
    conn.commit()
    conn.close()
    
def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    query = "DELETE FROM players;"
    c.execute(query)
    conn.commit()
    conn.close()

def countPlayers():    
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    query = "SELECT count(*) FROM players;"
    c.execute(query)
    results = c.fetchone()
    num_players = results[0]
    conn.close()    
    return num_players

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    query = "INSERT INTO players (name) VALUES (%s);" 
    c.execute(query, (name,))
    conn.commit()
    conn.close() 

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    query = "SELECT * FROM player_standings;"
    c.execute(query)
    results = c.fetchall()
    conn.close()    
    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()

    # string replacement preventing SQL injection
    query = "INSERT INTO matches (player1, player2, winner_id) VALUES (%s, %s, %s);" 
    c.execute(query, (winner, loser, winner))
    conn.commit()
    conn.close()     
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    query = "SELECT * FROM player_standings;"
    c.execute(query)
    results = c.fetchall()

    #setup 2 alternating lists for even numbers and odd numbers
    even_list = []
    odd_list = []

    # enumerate to get a row count
    # append tuple of id, name to even list or odd list
    for counter, record in enumerate(results):
        if counter % 2 == 0:
            even_list.append((record[0], record[1]))
        else:
            odd_list.append((record[0], record[1]))

    # zip the lists together
    zipped_list = zip(even_list, odd_list)

    # a + b combines contents of the 2 tuples
    pairings_list = []
    for a,b in zipped_list:
        pairings_list.append(a + b)

    #print pairings_list

    conn.close()    

    return pairings_list

