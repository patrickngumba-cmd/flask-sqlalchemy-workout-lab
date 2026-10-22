from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
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


# GET /workouts - List all workouts
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)


# GET /workouts/<id> - Show a single workout with its associated exercises and sets/reps/duration
@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    return make_response(jsonify(workout_schema.dump(workout)), 200)


# POST /workouts - Create a workout
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "No input data provided"}), 400)

    try:
        validated_data = workout_schema.load(data)
        new_workout = Workout(
            date=validated_data['date'],
            duration_minutes=validated_data['duration_minutes'],
            notes=validated_data.get('notes')
        )
        db.session.add(new_workout)
        db.session.commit()
        return make_response(jsonify(workout_schema.dump(new_workout)), 201)
    except (ValidationError, ValueError, IntegrityError) as err:
        db.session.rollback()
        messages = err.messages if isinstance(err, ValidationError) else str(err)
        return make_response(jsonify({"errors": messages}), 400)


# DELETE /workouts/<id> - Delete a workout and its associated WorkoutExercises
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({"message": f"Workout {id} deleted successfully"}), 200)


# GET /exercises - List all exercises
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


# GET /exercises/<id> - Show an exercise and associated workouts
@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    return make_response(jsonify(exercise_schema.dump(exercise)), 200)


# POST /exercises - Create an exercise
@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "No input data provided"}), 400)

    try:
        validated_data = exercise_schema.load(data)
        new_exercise = Exercise(
            name=validated_data['name'],
            category=validated_data['category'],
            equipment_needed=validated_data['equipment_needed']
        )
        db.session.add(new_exercise)
        db.session.commit()
        return make_response(jsonify(exercise_schema.dump(new_exercise)), 201)
    except (ValidationError, ValueError, IntegrityError) as err:
        db.session.rollback()
        messages = err.messages if isinstance(err, ValidationError) else str(err)
        return make_response(jsonify({"errors": messages}), 400)


# DELETE /exercises/<id> - Delete an exercise and associated WorkoutExercises
@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({"message": f"Exercise {id} deleted successfully"}), 200)


# POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises - Add an exercise to a workout
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    data = request.get_json() or {}

    try:
        validated_data = workout_exercise_schema.load(data)
        workout_exercise = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=exercise.id,
            sets=validated_data.get('sets'),
            reps=validated_data.get('reps'),
            duration_seconds=validated_data.get('duration_seconds')
        )
        db.session.add(workout_exercise)
        db.session.commit()
        return make_response(jsonify(workout_exercise_schema.dump(workout_exercise)), 201)
    except (ValidationError, ValueError, IntegrityError) as err:
        db.session.rollback()
        messages = err.messages if isinstance(err, ValidationError) else str(err)
        return make_response(jsonify({"errors": messages}), 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True, use_reloader=False)
