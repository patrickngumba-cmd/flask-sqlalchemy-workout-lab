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
    except (ValidationError, ValueError) as err:
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


if __name__ == '__main__':
    app.run(port=5555, debug=True)
