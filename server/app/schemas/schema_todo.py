from marshmallow.exceptions import ValidationError
from marshmallow import validates

from app import ma, models


class TodoSchema(ma.Schema):
    id = ma.Integer()
    title = ma.String(required=True)
    done = ma.Boolean()
    created_by = ma.UUID()

    @validates('title')
    def validate_title(self, title):
        if len(title) <= 0:
            raise ValidationError("This field can't be empty.")
        elif len(title) > 120:
            raise ValidationError('max character of 120 characters exceeded.')


todo_schema = TodoSchema()
todo_schemas = TodoSchema(many=True)
