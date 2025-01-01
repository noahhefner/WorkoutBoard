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

            # Insert data into the 'workout_sections' table
            cursor.executemany('''
                INSERT INTO workout_sections (workout_id, section_id, section_order)
                VALUES (?, ?, ?)
            ''', [
                (1, 1, 1),  # Full Body - Warm-up
                (1, 2, 2),  # Full Body - Strength Training
                (1, 5, 3),  # Full Body - Cooldown

                (2, 1, 1),  # Upper Body Strength - Warm-up
                (2, 2, 2),  # Upper Body Strength - Strength Training
                (2, 5, 3),  # Upper Body Strength - Cooldown

                (3, 1, 1),  # Cardio - Warm-up
                (3, 3, 2),  # Cardio - Conditioning
                (3, 4, 3),  # Cardio - Speed and Agility
                (3, 5, 4),  # Cardio - Cooldown
            ])

            # Insert data into the 'workout_movements' table
            cursor.executemany('''
                INSERT INTO workout_movements (workout_id, movement_id, section_id, movement_order, duration)
                VALUES (?, ?, ?, ?, ?)
            ''', [
                # Full Body - Warm-up
                (1, 5, 1, 1, 600),  # Treadmill - 10 minutes
                # Full Body - Strength Training
                (1, 4, 2, 1, 600),  # Pushup
                (1, 7, 2, 2, 600),  # Sit-ups
                (1, 1, 2, 3, 600),  # Squats
                (1, 8, 2, 4, 600),  # Lunges
                # Full Body - Cooldown
                (1, 6, 3, 1, 600),  # Rower Machine - 10 minutes
                
                # Upper Body Strength - Warm-up
                (2, 5, 1, 1, 300),  # Treadmill - 5 minutes
                # Upper Body Strength - Strength Training
                (2, 4, 2, 1, 300),  # Pushups - 5 minutes
                # Upper Body Strength - Cooldown
                (2, 6, 3, 1, 300),   # Rower Machine - 5 minutes

                # Cardio - Warm-up
                (3, 5, 1, 1, 300),  # Treadmill - 5 minutes
                # Upper Body Strength - Strength Training
                (3, 9, 2, 1, 300),  # Step-ups - 5 minutes
                (3, 10, 2, 3, 300), # Ladder in-and-outs - 5 minutes
                # Upper Body Strength - Cooldown
                (3, 6, 3, 1, 300)   # Rower Machine - 5 minutes
            ])
            
            # Commit the transaction
            conn.commit()

            print("Test data seeded!")

    except sqlite3.Error as e:
        print(f"SQLite error occurred: {e}")

if __name__ == "__main__":
    seed_data()
