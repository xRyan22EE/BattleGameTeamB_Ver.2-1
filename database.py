import sqlite3

# Database file name
DB_FILE = "battleship_game.db"

# Step 1: Initialize the database
def initialize_database():
    # Connect to the database (or create it if it doesn't exist)
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        # Create a table to store player statistics
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS player_stats (
            player_name TEXT UNIQUE,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0
        )
        """)
        connection.commit()

# Step 2: Add a new player
def add_player(player_name):
    # Add a new player to the database
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            INSERT INTO player_stats (player_name) 
            VALUES (?)
            """, (player_name,))
            connection.commit()
        except sqlite3.IntegrityError:
            return False

# Step 3: Record a win
def record_win(player_name):
    # Record a win for the specified player
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE player_stats
        SET wins = wins + 1
        WHERE player_name = ?
        """, (player_name,))
        connection.commit()

# Step 4: Record a loss
def record_loss(player_name):
    # Record a loss for the specified player
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE player_stats
        SET losses = losses + 1
        WHERE player_name = ?
        """, (player_name,))
        connection.commit()

# Step 5: Retrieve player stats
def get_player_stats(player_name):
    # Retrieve stats for a specific player
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT wins, losses
        FROM player_stats
        WHERE player_name = ?
        """, (player_name,))
        stats = cursor.fetchone()
        if stats:
            return stats[0],stats[1]
        else:

            return None, None

# Initialize the database at the start
initialize_database()