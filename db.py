import sqlite3
import os
from flask import current_app

def init_db():
    """Initialize the database and create tables."""
    db_path = os.path.join(current_app.instance_path, 'workout_app.db')
    
    # Connect to SQLite database (it will create the file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the 'workouts' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_name TEXT NOT NULL,
            description TEXT
        );
    ''')

    # Create the 'movements' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movements (
            movement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            movement_name TEXT NOT NULL,
            description TEXT
        );
    ''')

    # Create the 'workout_movements' junction table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_movements (
            workout_id INTEGER,
            movement_id INTEGER,
            reps INTEGER,          -- Optional: number of repetitions for this movement in the workout
            duration INTEGER,      -- Optional: duration in seconds for this movement in the workout
            PRIMARY KEY (workout_id, movement_id),
            FOREIGN KEY (workout_id) REFERENCES workouts(workout_id) ON DELETE CASCADE,
            FOREIGN KEY (movement_id) REFERENCES movements(movement_id) ON DELETE CASCADE
        );
    ''')

    # Commit the transaction to save changes
    conn.commit()
    conn.close()

    print("Database and tables created successfully!")
