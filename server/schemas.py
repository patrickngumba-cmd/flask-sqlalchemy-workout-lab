from marshmallow import Schema, fields, validates, validates_schema, ValidationError
from models import VALID_CATEGORIES


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)

    # Include nested exercise details when viewing a workout's exercises
    exercise = fields.Nested(lambda: ExerciseSchema(only=("id", "name", "category", "equipment_needed")), dump_only=True)

    @validates_schema
    def validate_workout_exercise_metrics(self, data, **kwargs):
        reps = data.get("reps")
        sets = data.get("sets")
        duration = data.get("duration_seconds")

        if reps is None and sets is None and duration is None:
            raise ValidationError("Must provide sets/reps or duration_seconds for a workout exercise.")

        if sets is not None and sets <= 0:
            raise ValidationError("Sets must be greater than 0.")
        if reps is not None and reps <= 0:
            raise ValidationError("Reps must be greater than 0.")
        if duration is not None and duration <= 0:
            raise ValidationError("Duration in seconds must be greater than 0.")


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)

    # Associated workouts for GET /exercises/<id>
    workouts = fields.List(fields.Nested(lambda: WorkoutSchema(exclude=("exercises", "workout_exercises"))), dump_only=True)

    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value or len(value.strip()) < 2:
            raise ValidationError("Exercise name must be at least 2 characters long.")

    @validates("category")
    def validate_category(self, value, **kwargs):
        if value not in VALID_CATEGORIES:
            raise ValidationError(f"Category must be one of: {', '.join(VALID_CATEGORIES)}")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(allow_none=True)

    # Stretch goal: include reps/sets/duration data from WorkoutExercises
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)
    exercises = fields.List(fields.Nested(lambda: ExerciseSchema(exclude=("workouts",))), dump_only=True)

    @validates("duration_minutes")
    def validate_duration(self, value, **kwargs):
        if value is None or value <= 0:
            raise ValidationError("Workout duration_minutes must be greater than 0.")


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=("workout_exercises",))
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True, exclude=("workouts",))
workout_exercise_schema = WorkoutExerciseSchema()
