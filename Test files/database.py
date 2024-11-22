# database.py
import sqlite3

# Connect to the database (or create it if it doesn't exist)
def initialize_database():
    conn = sqlite3.connect("game_stats.db")
    cursor = conn.cursor()
    # Create a table to store wins and losses if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0
        )
    """)
    # Insert initial stats row if table is empty
    cursor.execute("SELECT COUNT(*) FROM stats")#COUNT(*) returns the number of rows in the stats table.
    if cursor.fetchone()[0] == 0:#cursor.fetchone() retrieves the result of the previous SELECT query, only one element .
        cursor.execute("INSERT INTO stats (wins, losses) VALUES (0, 0)")#This ensures that the table has a starting record to keep track of wins and losses.
    conn.commit()
    conn.close()

# Function to add a win
def add_win():
    conn = sqlite3.connect("game_stats.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE stats SET wins = wins + 1 WHERE id = 1")
    conn.commit()
    conn.close()

# Function to add a loss
def add_loss():
    conn = sqlite3.connect("game_stats.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE stats SET losses = losses + 1 WHERE id = 1")
    conn.commit()# saves the changes to the database.
    conn.close()

# Function to retrieve the current stats
def get_stats():
    conn = sqlite3.connect("game_stats.db")
    cursor = conn.cursor()
    cursor.execute("SELECT wins, losses FROM stats WHERE id = 1")
    stats = cursor.fetchone()
    conn.close()
    if stats:
        return {"wins": stats[0], "losses": stats[1]}
    return {"wins": 0, "losses": 0}



#example of using it in the battle ship game 

# # main_game.py
# from database import initialize_database, add_win, add_loss, get_stats

# # Initialize the database at the start of the game
# initialize_database()

# # Function to display stats to the player
# def display_stats():
#     stats = get_stats()
#     print(f"Wins: {stats['wins']}, Losses: {stats['losses']}")

# # Example usage when player wins
# def player_wins():
#     print("Congratulations! You've won!")
#     add_win()  # Record the win in the database
#     display_stats()  # Show updated stats

# # Example usage when player loses
# def player_loses():
#     print("Game Over. You've lost!")
#     add_loss()  # Record the loss in the database
#     display_stats()  # Show updated stats
