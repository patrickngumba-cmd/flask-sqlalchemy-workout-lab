import pytest
from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        WorkoutExercise.query.delete()
        Workout.query.delete()
        Exercise.query.delete()
        db.session.commit()

        ex1 = Exercise(name="Barbell Squat", category="Strength", equipment_needed=True)
        ex2 = Exercise(name="Burpees", category="HIIT", equipment_needed=False)
        w1 = Workout(date=date(2026, 10, 20), duration_minutes=45, notes="Strength session")
        db.session.add_all([ex1, ex2, w1])
        db.session.commit()

        we1 = WorkoutExercise(workout_id=w1.id, exercise_id=ex1.id, sets=4, reps=10)
        db.session.add(we1)
        db.session.commit()

        with app.test_client() as client:
            yield client


def test_get_workouts(client):
    res = client.get('/workouts')
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 1
    assert data[0]['duration_minutes'] == 45


def test_get_single_workout(client):
    res = client.get('/workouts/1')
    assert res.status_code == 200
    data = res.get_json()
    assert data['id'] == 1
    assert len(data['workout_exercises']) == 1


def test_create_workout_validation(client):
    valid_res = client.post('/workouts', json={
        "date": "2026-10-21",
        "duration_minutes": 30,
        "notes": "Morning run"
    })
    assert valid_res.status_code == 201

    invalid_res = client.post('/workouts', json={
        "date": "2026-10-21",
        "duration_minutes": -10,
        "notes": "Invalid"
    })
    assert invalid_res.status_code == 400


def test_delete_workout(client):
    res = client.delete('/workouts/1')
    assert res.status_code == 200
    check = client.get('/workouts/1')
    assert check.status_code == 404


def test_exercises_endpoints(client):
    get_res = client.get('/exercises')
    assert get_res.status_code == 200
    assert len(get_res.get_json()) == 2

    post_res = client.post('/exercises', json={
        "name": "Kettlebell Swing",
        "category": "HIIT",
        "equipment_needed": True
    })
    assert post_res.status_code == 201


def test_add_exercise_to_workout(client):
    res = client.post('/workouts/1/exercises/2/workout_exercises', json={
        "sets": 3,
        "reps": 15
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data['sets'] == 3


def test_model_validations():
    with app.app_context():
        with pytest.raises(ValueError):
            Exercise(name="A", category="Strength", equipment_needed=False)

        with pytest.raises(ValueError):
            Workout(date=date(2026, 10, 20), duration_minutes=0, notes="Invalid")