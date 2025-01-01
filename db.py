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
                    workout_description TEXT
                );
            ''')

            # Create movements table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movements (
                    movement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    movement_name TEXT NOT NULL,
                    movement_description TEXT
                );
            ''')

            # Create sections table
            cursor.execute('''
                CREATE TABLE sections (
                    section_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    section_name TEXT NOT NULL
                );
            ''')

            # Create workout_sections table
            cursor.execute('''
                CREATE TABLE workout_sections (
                    workout_section_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workout_id INTEGER NOT NULL,
                    section_id INTEGER NOT NULL,
                    section_order INTEGER NOT NULL,
                    FOREIGN KEY (workout_id) REFERENCES workouts(workout_id) ON DELETE CASCADE,
                    FOREIGN KEY (section_id) REFERENCES sections(section_id) ON DELETE CASCADE
                );
            ''')

            # Create workout_movements table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workout_movements (
                    workout_id INTEGER,
                    movement_id INTEGER,
                    section_id INTEGER,
                    movement_order INTEGER,
                    duration INTEGER,
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

            # SQL query to retrieve workouts, sections, and movements
            query = '''
                SELECT 
                    workouts.workout_id, workouts.workout_name, workouts.workout_description,
                    sections.section_id, sections.section_name, workout_sections.section_order,
                    movements.movement_id, movements.movement_name, movements.movement_description AS movement_description,
                    workout_movements.movement_order, workout_movements.duration
                FROM workouts
                LEFT JOIN workout_sections ON workouts.workout_id = workout_sections.workout_id
                LEFT JOIN sections ON workout_sections.section_id = sections.section_id
                LEFT JOIN workout_movements 
                    ON workouts.workout_id = workout_movements.workout_id 
                    AND workout_sections.section_id = workout_movements.section_id
                LEFT JOIN movements ON workout_movements.movement_id = movements.movement_id
                ORDER BY workouts.workout_id, workout_sections.section_order, workout_movements.movement_order
            '''

            cursor.execute(query)
            results = cursor.fetchall()

            # Organize the results into a structured format
            workouts = {}
            for row in results:
                workout_id = row[0]
                workout_name = row[1]
                workout_description = row[2]
                section_id = row[3]
                section_name = row[4]
                section_order = row[5]
                movement_id = row[6]
                movement_name = row[7]
                movement_description = row[8]
                movement_order = row[9]
                duration = row[10]

                if workout_id not in workouts:
                    workouts[workout_id] = {
                        'workout_id': workout_id,
                        'workout_name': workout_name,
                        'workout_description': workout_description,
                        'sections': []
                    }

                workout = workouts[workout_id]

                # Add the section if not already present
                section = next((s for s in workout['sections'] if s['section_id'] == section_id), None)
                if section is None:
                    section = {
                        'section_id': section_id,
                        'section_name': section_name,
                        'section_order': section_order,
                        'movements': []
                    }
                    workout['sections'].append(section)

                # Add the movement if it exists (movement_id is not None)
                if movement_id is not None:
                    section['movements'].append({
                        'movement_id': movement_id,
                        'movement_name': movement_name,
                        'movement_description': movement_description,
                        'movement_order': movement_order,
                        'duration': duration
                    })

            # Sort sections and movements by their order
            for workout in workouts.values():
                workout['sections'].sort(key=lambda s: s['section_order'])
                for section in workout['sections']:
                    section['movements'].sort(key=lambda m: m['movement_order'])

            # Convert the dictionary to a list
            workout_list = list(workouts.values())
            
            return workout_list

    except sqlite3.Error as e:
        current_app.logger.error(f"SQLite error occurred: {e}")
        return []  # Return an empty list if there's an error



def get_workout_by_id(workout_id):
    db_path = os.path.join(current_app.instance_path, 'workouts.db')

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # SQL query to retrieve the workout, its sections, and associated movements
            query = '''
                SELECT 
                    workouts.workout_id, workouts.workout_name, workouts.workout_description,
                    sections.section_id, sections.section_name, workout_sections.section_order,
                    movements.movement_id, movements.movement_name, movements.movement_description AS movement_description,
                    workout_movements.movement_order, workout_movements.duration
                FROM workouts
                LEFT JOIN workout_sections ON workouts.workout_id = workout_sections.workout_id
                LEFT JOIN sections ON workout_sections.section_id = sections.section_id
                LEFT JOIN workout_movements 
                    ON workouts.workout_id = workout_movements.workout_id 
                    AND workout_sections.section_id = workout_movements.section_id
                LEFT JOIN movements ON workout_movements.movement_id = movements.movement_id
                WHERE workouts.workout_id = ?
                ORDER BY workout_sections.section_order, workout_movements.movement_order
            '''

            cursor.execute(query, (workout_id,))
            results = cursor.fetchall()

            if not results:
                return None  # Return None if the workout is not found

            # Organize the results into a structured workout dictionary
            workout = {
                'workout_id': results[0][0],
                'workout_name': results[0][1],
                'description': results[0][2],
                'sections': []
            }

            sections = {}
            for row in results:
                section_id = row[3]
                section_name = row[4]
                section_order = row[5]
                movement_id = row[6]
                movement_name = row[7]
                movement_description = row[8]
                movement_order = row[9]
                duration = row[10]

                # Add the section if not already present
                if section_id not in sections:
                    sections[section_id] = {
                        'section_id': section_id,
                        'section_name': section_name,
                        'section_order': section_order,
                        'movements': []
                    }
                    workout['sections'].append(sections[section_id])

                # Add the movement to the corresponding section if it exists
                if movement_id is not None:
                    sections[section_id]['movements'].append({
                        'movement_id': movement_id,
                        'movement_name': movement_name,
                        'movement_description': movement_description,
                        'movement_order': movement_order,
                        'duration': duration
                    })

            # Sort sections and movements by their respective orders
            workout['sections'].sort(key=lambda s: s['section_order'])
            for section in workout['sections']:
                section['movements'].sort(key=lambda m: m['movement_order'])

            return workout

    except sqlite3.Error as e:
        current_app.logger.error(f"SQLite error occurred: {e}")
        return None  # Return None if there's an error
