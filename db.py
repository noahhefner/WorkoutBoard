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

            # Create sections table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sections (
                    section_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    section_name TEXT NOT NULL
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

            # Create workout_movements table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workouts_movements (
                    workouts_movements_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workout_id INTEGER NOT NULL,
                    section_id INTEGER NOT NULL,
                    section_order INTEGER NOT NULL,
                    movement_id INTEGER NOT NULL,
                    movement_order INTEGER NOT NULL,
                    movement_duration INTEGER NOT NULL,
                    FOREIGN KEY (workout_id) REFERENCES workouts(workout_id) ON DELETE CASCADE,
                    FOREIGN KEY (section_id) REFERENCES sections(section_id) ON DELETE CASCADE,
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
                    sections.section_id, sections.section_name, workouts_movements.section_order,
                    movements.movement_id, movements.movement_name, movements.movement_description, workouts_movements.movement_order, workouts_movements.movement_duration
                FROM workouts
                LEFT JOIN workouts_movements ON workouts.workout_id = workouts_movements.workout_id
                LEFT JOIN sections ON sections.section_id = workouts_movements.section_id
                LEFT JOIN movements ON movements.movement_id = workouts_movements.movement_id
                ORDER BY workouts.workout_id, workouts_movements.section_order, workouts_movements.movement_order
            '''

            cursor.execute(query)
            results = cursor.fetchall()

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
                movement_duration = row[10]

                if workout_id not in workouts:
                    workouts[workout_id] = {
                        'workout_id': workout_id,
                        'workout_name': workout_name,
                        'workout_description': workout_description,
                        'sections': []
                    }

                workout = workouts[workout_id]

                section = None
                for s in workout['sections']:
                    if s['section_id'] == section_id:
                        section = s
                        break
                if section is None:
                    section = {
                        'section_id': section_id,
                        'section_name': section_name,
                        'section_order': section_order,
                        'movements': []
                    }
                    workout['sections'].append(section)

                if movement_id is not None:
                    section['movements'].append({
                        'movement_id': movement_id,
                        'movement_name': movement_name,
                        'movement_description': movement_description,
                        'movement_order': movement_order,
                        'movement_duration': movement_duration
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

            query = '''
                SELECT 
                    workouts.workout_id, workouts.workout_name, workouts.workout_description,
                    sections.section_id, sections.section_name, workouts_movements.section_order,
                    movements.movement_id, movements.movement_name, movements.movement_description, workouts_movements.movement_order, workouts_movements.movement_duration
                FROM workouts
                LEFT JOIN workouts_movements ON workouts.workout_id = workouts_movements.workout_id
                LEFT JOIN sections ON sections.section_id = workouts_movements.section_id
                LEFT JOIN movements ON movements.movement_id = workouts_movements.movement_id
                WHERE workouts.workout_id = ?
                ORDER BY workouts_movements.section_order, workouts_movements.movement_order
            '''

            cursor.execute(query, (workout_id,))
            results = cursor.fetchall()

            if not results:
                return None  # Return None if the workout is not found

            # Organize the results into a structured workout dictionary
            workout = {
                'total_duration': 0,
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
                movement_duration = row[10]

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
                        'movement_duration': movement_duration
                    })
                    workout['total_duration'] += int(movement_duration)

            # Sort sections and movements by their respective orders
            workout['sections'].sort(key=lambda s: s['section_order'])
            for section in workout['sections']:
                section['movements'].sort(key=lambda m: m['movement_order'])

            return workout

    except sqlite3.Error as e:
        current_app.logger.error(f"SQLite error occurred: {e}")
        return None  # Return None if there's an error
