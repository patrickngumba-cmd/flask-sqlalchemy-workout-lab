# Flask SQLAlchemy Workout Application Backend

## Project Description
A RESTful backend API built with Flask, SQLAlchemy, Flask-Migrate, and Marshmallow for personal trainers to track workouts and reusable exercises. It includes table constraints, SQLAlchemy model validations, and Marshmallow schema validations.

## Installation Instructions

1. Clone this repository and navigate to the project folder:
   bash
   git clone [https://github.com/patrickngumba-cmd/flask-sqlalchemy-workout-lab.git]
   cd flask-sqlalchemy-workout-lab
   

2. Install dependencies and activate the virtual environment:
   bash
   pipenv install
   pipenv shell

   *(Or if using standard `venv` on Windows):*
   powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install flask flask-sqlalchemy flask-migrate marshmallow pytest
   

3. Run the database migrations:
   bash
   cd server
   flask --app app.py db upgrade head
   

4. Seed the database with initial sample data:
   bash
   python seed.py
   

## Run Instructions

From the `server` folder, start the Flask server (runs on port `5555`):
bash
python app.py

Or using the Flask command:
bash
flask --app app.py run --port 5555


To run the automated tests from the root project folder:
bash
pytest


## API Endpoints

### Workouts
- **`GET /workouts`** - List all workouts.
- **`GET /workouts/<id>`** - View a single workout by ID along with its associated exercises and sets/reps/duration data.
- **`POST /workouts`** - Create a new workout (`date`, `duration_minutes`, `notes`).
- **`DELETE /workouts/<id>`** - Delete a workout by ID and cascade delete its associated `WorkoutExercises`.

### Exercises
- **`GET /exercises`** - List all exercises.
- **`GET /exercises/<id>`** - View a single exercise by ID along with its associated workouts.
- **`POST /exercises`** - Create a new exercise (`name`, `category`, `equipment_needed`).
- **`DELETE /exercises/<id>`** - Delete an exercise by ID and cascade delete its associated `WorkoutExercises`.

### Workout Exercises
- **`POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`** - Add an exercise to a workout with `sets`, `reps`, and/or `duration_seconds`.