from sqlalchemy import create_engine, MetaData, Table

engine = create_engine('sqlite:///instance/workout_app.db')

metadata = MetaData()
metadata.bind = engine

workouts_table = Table('workouts', metadata, autoload_with=engine)
movements_table = Table('movements', metadata, autoload_with=engine)
workout_movements_table = Table('workout_movements', metadata, autoload_with=engine)

def seed_data():
    connection = engine.connect()

    # Insert workouts
    connection.execute(workouts_table.insert(), [
        {"workout_name": "Full Body Blast"},
        {"workout_name": "Upper Body Strength"}
    ])

    # Insert movements
    connection.execute(movements_table.insert(), [
        {"movement_name": "Squat"},
        {"movement_name": "Deadlift"},
        {"movement_name": "Plank"}
    ])

    # Insert workout movements
    connection.execute(workout_movements_table.insert(), [
        {"workout_id": 1, "movement_id": 1, "reps": 12, "sets": 3, "duration": None},
        {"workout_id": 1, "movement_id": 2, "reps": 10, "sets": 3, "duration": None},
        {"workout_id": 1, "movement_id": 3, "reps": None, "sets": 3, "duration": "00:01:00"}
    ])

    print("Test data seeded!")

if __name__ == "__main__":
    seed_data()
