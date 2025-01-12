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
                INSERT INTO workouts (workout_name, workout_description) 
                VALUES (?, ?)
            ''', [
                ("Full Body", "A comprehensive full body workout."),
                ("Upper Body Strength", "Focuses on upper body strength and endurance."),
                ("Cardio", "High intensity interval training.")
            ])

            
            # Insert data into the 'sections' table
            cursor.executemany('''
                INSERT INTO sections (section_name)
                VALUES (?)
            ''', [
                ("Warm-up",),
                ("Strenth Training",),
                ("Conditioning",),
                ("Speed and Agility",),
                ("Cooldown",)
            ])

            
            # Insert data into the 'movements' table
            cursor.executemany('''
                INSERT INTO movements (movement_name, movement_description)
                VALUES (?, ?)
            ''', [
                ("Squat", "A lower body strength exercise focusing on thighs and glutes."),
                ("Deadlift", "A weightlifting movement that targets the back and legs."),
                ("Plank", "A core strengthening exercise involving a static hold."),
                ("Pushup", "A chest exercise."),
                ("Treadmill", "Run on the treadmill."),
                ("Rower Machine", "Row at a moderate pace."),
                ("Sit-ups", "Do standard sit-ups."),
                ("Lunges", "Alternating lunges."),
                ("Step-Ups", "Fast-paced lower body mobility."),
                ("Ladder In-and-Outs", "Fast footwork.")
            ])

            # Insert data into the 'workout_movements' table
            cursor.executemany('''
                INSERT INTO workouts_movements (workout_id, section_id, section_order, movement_id, movement_order, movement_duration)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', [
                # Full Body - Warm-up
                (1, 1, 1, 5, 1, 600),             # Treadmill
                # Full Body - Strength Training
                (1, 2, 1, 4, 1, 600),             # Pushup
                # Full Body - Cooldown
                (1, 5, 1, 3, 1, 600),             # Plank
            ])
            
            # Commit the transaction
            conn.commit()

            print("Test data seeded!")

    except sqlite3.Error as e:
        print(f"SQLite error occurred: {e}")

if __name__ == "__main__":
    seed_data()
