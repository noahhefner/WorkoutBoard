import sqlite3
import os

def seed_data():

    db_path = "./instance/workouts.db"

    try:
        # Connect to the SQLite database
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Insert data into the 'workouts' table
            cursor.executemany('''
                INSERT INTO workouts (workout_name, description) 
                VALUES (?, ?)
            ''', [
                ("Full Body Blast", "A comprehensive full body workout."),
                ("Upper Body Strength", "Focuses on upper body strength and endurance.")
            ])

            # Insert data into the 'movements' table
            cursor.executemany('''
                INSERT INTO movements (movement_name, description)
                VALUES (?, ?)
            ''', [
                ("Squat", "A lower body strength exercise focusing on thighs and glutes."),
                ("Deadlift", "A weightlifting movement that targets the back and legs."),
                ("Plank", "A core strengthening exercise involving a static hold."),
                ("Pushup", "A chest exercise.")
            ])

            # Insert data into the 'workout_movements' table
            cursor.executemany('''
                INSERT INTO workout_movements (workout_id, movement_id, reps, sets, duration)
                VALUES (?, ?, ?, ?, ?)
            ''', [
                (1, 1, 12, 3, None),         # Workout 1 - Squat
                (1, 2, 10, 3, None),         # Workout 1 - Deadlift
                (1, 3, None, 3, '00:01:00'), # Workout 1 - Plank
                (2, 4, 10, 3, None)          # Workout 2 - Pushup
            ])

            # Commit the transaction
            conn.commit()

            print("Test data seeded!")

    except sqlite3.Error as e:
        print(f"SQLite error occurred: {e}")

if __name__ == "__main__":
    seed_data()
