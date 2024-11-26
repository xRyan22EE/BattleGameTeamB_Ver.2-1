import sqlite3
import logging
import os

# Define the database file path
DATABASE_FILE = os.path.join(os.path.dirname(__file__), 'battleship_game.db')

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Initialize the database
def initialize_database():
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
        
        # Connect to the database (or create it if it doesn't exist)
        with sqlite3.connect(DATABASE_FILE) as connection:
            cursor = connection.cursor()
            # Create a table to store player statistics
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS player_stats (
                player_name TEXT UNIQUE,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0
            )
            """)

            # Commit the transaction
            connection.commit()
    except sqlite3.Error as e: # Catch any exceptions
        logging.error(f"Error initializing database: {e}")

def reset_database():
    try:
        # Delete the old database file if it exists
        if os.path.exists(DATABASE_FILE):
            os.remove(DATABASE_FILE)
            logging.info(f"Deleted old database file: {DATABASE_FILE}")
        
        # Initialize a new database
        initialize_database()
        logging.info("Created a new database.")
    except Exception as e:
        logging.error(f"Error resetting database: {e}")


# Step 2: Implement the database functions
def add_player(player_name):
    try:
        # Add a new player to the database
        with sqlite3.connect(DATABASE_FILE) as connection: # Connect to the database
            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()

            # Insert the player into the database
            cursor.execute("""
            INSERT INTO player_stats (player_name) 
            VALUES (?)
            """, (player_name,))
            connection.commit()
        return True
    except sqlite3.IntegrityError: # Catch the exception if the player already exists
        logging.warning(f"Player {player_name} already exists.")
        return False
    except sqlite3.Error as e: # Catch any other exceptions
        logging.error(f"Error adding player: {e}")
        return False

def record_win(player_name):
    try:
        # Record a win for the specified player
        with sqlite3.connect(DATABASE_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("""
            UPDATE player_stats
            SET wins = wins + 1
            WHERE player_name = ?
            """, (player_name,))
            connection.commit()
    except sqlite3.Error as e:
        logging.error(f"Error recording win: {e}")

def record_loss(player_name):
    try:
        # Record a loss for the specified player
        with sqlite3.connect(DATABASE_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("""
            UPDATE player_stats
            SET losses = losses + 1
            WHERE player_name = ?
            """, (player_name,))
            connection.commit()
    except sqlite3.Error as e:
        logging.error(f"Error recording loss: {e}")

def get_player_stats(player_name):
    try:
        # Retrieve stats for a specific player
        with sqlite3.connect(DATABASE_FILE) as connection: 
            cursor = connection.cursor()
            cursor.execute("""
            SELECT wins, losses
            FROM player_stats
            WHERE player_name = ?
            """, (player_name,))
            stats = cursor.fetchone()
            if stats:
                return stats[0], stats[1]
            else:
                return None, None
    except sqlite3.Error as e:
        logging.error(f"Error retrieving player stats: {e}")
        return None, None

# Initialize the database at the start
initialize_database()
reset_database()