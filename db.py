import sqlite3
import os
from flask import current_app

def init_db():

    db_path = os.path.join(current_app.instance_path, 'workouts.db')

    try:

        with sqlite3.connect(db_path) as conn:

            cursor = conn.cursor()

            # Create workouts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workouts (
                    workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workout_name TEXT NOT NULL,
                    description TEXT
                );
            ''')

            # Create movements table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movements (
                    movement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    movement_name TEXT NOT NULL,
                    description TEXT
                );
            ''')

            # Create workout_movements table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workout_movements (
                    workout_id INTEGER,
                    movement_id INTEGER,
                    reps INTEGER,          -- Optional: number of repetitions for this movement in the workout
                    sets INTEGER,
                    duration INTEGER,      -- Optional: duration in seconds for this movement in the workout
                    PRIMARY KEY (workout_id, movement_id),
                    FOREIGN KEY (workout_id) REFERENCES workouts(workout_id) ON DELETE CASCADE,
                    FOREIGN KEY (movement_id) REFERENCES movements(movement_id) ON DELETE CASCADE
                );
            ''')

            # Commit is done automatically by the `with` block
            current_app.logger.info("Database and tables created successfully!")

    except sqlite3.Error as e:

        current_app.logger.error(f"SQLite error occurred: {e}")


def get_all_workouts():
    
    db_path = os.path.join(current_app.instance_path, 'workouts.db')

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # SQL query to retrieve workouts along with their associated movements
            query = '''
                SELECT workouts.workout_id, workouts.workout_name, workouts.description,
                       movements.movement_id, movements.movement_name, movements.description AS movement_description,
                       workout_movements.reps, workout_movements.sets, workout_movements.duration
                FROM workouts
                LEFT JOIN workout_movements ON workouts.workout_id = workout_movements.workout_id
                LEFT JOIN movements ON workout_movements.movement_id = movements.movement_id
            '''

            cursor.execute(query)
            results = cursor.fetchall()

            # Organize the results into a list of workouts with their movements
            workouts = {}
            for row in results:
                workout_id = row[0]
                workout_name = row[1]
                workout_description = row[2]
                movement_id = row[3]
                movement_name = row[4]
                movement_description = row[5]
                reps = row[6]
                sets = row[7]
                duration = row[8]

                if workout_id not in workouts:
                    workouts[workout_id] = {
                        'workout_id': workout_id,
                        'workout_name': workout_name,
                        'description': workout_description,
                        'movements': []
                    }

                if movement_id is not None:
                    workouts[workout_id]['movements'].append({
                        'movement_id': movement_id,
                        'movement_name': movement_name,
                        'movement_description': movement_description,
                        'reps': reps,
                        'sets': sets,
                        'duration': duration
                    })

            # Convert the dictionary to a list
            workout_list = list(workouts.values())

            return workout_list

    except sqlite3.Error as e:
        current_app.logger.error(f"SQLite error occurred: {e}")
        return []  # Return an empty list if there's an error
