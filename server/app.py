from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    workout_schema,
    workouts_schema,
    exercise_schema,
    exercises_schema,
    workout_exercise_schema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


# List all workouts
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)


# Get a single workout with its exercises and sets/reps/duration
@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    workout = Workout.query.filter_by(id=id).first()
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    return make_response(jsonify(workout_schema.dump(workout)), 200)


# Create a new workout
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "No input data provided"}), 400)

    try:
        validated = workout_schema.load(data)
        new_workout = Workout(
            date=validated['date'],
            duration_minutes=validated['duration_minutes'],
            notes=validated.get('notes')
        )
        db.session.add(new_workout)
        db.session.commit()
        return make_response(jsonify(workout_schema.dump(new_workout)), 201)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)
    except Exception as err:
        db.session.rollback()
        return make_response(jsonify({"errors": str(err)}), 400)


# Delete a workout
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.filter_by(id=id).first()
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({"message": "Workout deleted"}), 200)


# List all exercises
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


# Get a single exercise and its workouts
@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    exercise = Exercise.query.filter_by(id=id).first()
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    return make_response(jsonify(exercise_schema.dump(exercise)), 200)


# Create a new exercise
@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "No input data provided"}), 400)

    try:
        validated = exercise_schema.load(data)
        new_exercise = Exercise(
            name=validated['name'],
            category=validated['category'],
            equipment_needed=validated['equipment_needed']
        )
        db.session.add(new_exercise)
        db.session.commit()
        return make_response(jsonify(exercise_schema.dump(new_exercise)), 201)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)
    except Exception as err:
        db.session.rollback()
        return make_response(jsonify({"errors": str(err)}), 400)


# Delete an exercise
@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.filter_by(id=id).first()
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({"message": "Exercise deleted"}), 200)


# Add an exercise to a workout
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.filter_by(id=workout_id).first()
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    exercise = Exercise.query.filter_by(id=exercise_id).first()
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "No input data provided"}), 400)

    try:
        validated = workout_exercise_schema.load(data)
        record = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=exercise.id,
            sets=validated.get('sets'),
            reps=validated.get('reps'),
            duration_seconds=validated.get('duration_seconds')
        )
        db.session.add(record)
        db.session.commit()
        return make_response(jsonify(workout_exercise_schema.dump(record)), 201)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)
    except Exception as err:
        db.session.rollback()
        return make_response(jsonify({"errors": str(err)}), 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)