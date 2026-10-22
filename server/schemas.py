from marshmallow import Schema, fields, validates, validates_schema, ValidationError
from models import VALID_CATEGORIES


# Basic schema used when nesting inside other schemas
class PlainExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)


class PlainWorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(allow_none=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)

    exercise = fields.Nested(PlainExerciseSchema, dump_only=True)

    @validates_schema
    def validate_metrics(self, data, **kwargs):
        reps = data.get("reps")
        sets = data.get("sets")
        duration = data.get("duration_seconds")

        if reps is None and sets is None and duration is None:
            raise ValidationError("Provide sets/reps or duration_seconds.")

        if sets is not None and sets <= 0:
            raise ValidationError("Sets must be greater than 0.")
        if reps is not None and reps <= 0:
            raise ValidationError("Reps must be greater than 0.")
        if duration is not None and duration <= 0:
            raise ValidationError("Duration must be greater than 0.")


class ExerciseSchema(PlainExerciseSchema):
    workouts = fields.List(fields.Nested(PlainWorkoutSchema), dump_only=True)

    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value or len(value.strip()) < 2:
            raise ValidationError("Exercise name must be at least 2 characters.")

    @validates("category")
    def validate_category(self, value, **kwargs):
        if value not in VALID_CATEGORIES:
            raise ValidationError("Invalid category.")


class WorkoutSchema(PlainWorkoutSchema):
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)
    exercises = fields.List(fields.Nested(PlainExerciseSchema), dump_only=True)

    @validates("duration_minutes")
    def validate_duration(self, value, **kwargs):
        if value is None or value <= 0:
            raise ValidationError("Duration must be greater than 0.")


workout_schema = WorkoutSchema()
workouts_schema = PlainWorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = PlainExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()