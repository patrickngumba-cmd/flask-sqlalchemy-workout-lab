#!/usr/bin/env python3

from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print("Clearing existing database records...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("Seeding exercises...")
    ex1 = Exercise(name="Barbell Back Squat", category="Strength", equipment_needed=True)
    ex2 = Exercise(name="Push-Ups", category="Strength", equipment_needed=False)
    ex3 = Exercise(name="Kettlebell Swings", category="HIIT", equipment_needed=True)
    ex4 = Exercise(name="Karura Trail Interval Run", category="Cardio", equipment_needed=False)
    ex5 = Exercise(name="Dynamic Hip Mobility Flow", category="Mobility", equipment_needed=False)

    db.session.add_all([ex1, ex2, ex3, ex4, ex5])
    db.session.commit()

    print("Seeding workouts...")
    w1 = Workout(
        date=date(2026, 10, 15),
        duration_minutes=60,
        notes="Lower body strength focus and core conditioning"
    )
    w2 = Workout(
        date=date(2026, 10, 17),
        duration_minutes=45,
        notes="Morning cardio and kettlebell conditioning circuit"
    )
    w3 = Workout(
        date=date(2026, 10, 19),
        duration_minutes=30,
        notes="Active recovery and mobility session"
    )

    db.session.add_all([w1, w2, w3])
    db.session.commit()

    print("Linking exercises to workouts...")
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=ex1.id, sets=4, reps=8, duration_seconds=None)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=ex2.id, sets=3, reps=15, duration_seconds=None)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=ex4.id, sets=1, reps=1, duration_seconds=1200)
    we4 = WorkoutExercise(workout_id=w2.id, exercise_id=ex3.id, sets=4, reps=12, duration_seconds=180)
    we5 = WorkoutExercise(workout_id=w3.id, exercise_id=ex5.id, sets=2, reps=10, duration_seconds=600)

    db.session.add_all([we1, we2, we3, we4, we5])
    db.session.commit()

    print("Database seeded successfully!")
