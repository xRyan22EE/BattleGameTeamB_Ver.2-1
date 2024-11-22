# test_database.py
from database import initialize_database, add_win, add_loss, get_stats

# Step 1: Initialize the database
print("Initializing database...")
initialize_database()

# Step 2: Display initial stats
print("Initial stats:")
initial_stats = get_stats()
print(f"Wins: {initial_stats['wins']}, Losses: {initial_stats['losses']}")

# Step 3: Add a win and display stats
print("\nAdding a win...")
add_win()
stats_after_win = get_stats()
print(f"Wins after adding a win: {stats_after_win['wins']}, Losses: {stats_after_win['losses']}")

# Step 4: Add a loss and display stats
print("\nAdding a loss...")
add_loss()
stats_after_loss = get_stats()
print(f"Wins: {stats_after_loss['wins']}, Losses after adding a loss: {stats_after_loss['losses']}")

# Step 5: Add multiple wins and losses and display final stats
print("\nAdding multiple wins and losses...")
for _ in range(3):
    add_win()
for _ in range(2):
    add_loss()

final_stats = get_stats()
print(f"Final Stats - Wins: {final_stats['wins']}, Losses: {final_stats['losses']}")
