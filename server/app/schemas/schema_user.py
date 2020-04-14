from marshmallow.exceptions import ValidationError
from marshmallow import validates

from app import ma, models
from app.schemas.schema_todo import TodoSchema


class UserSchema(ma.Schema):
    public_id = ma.UUID()
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    email = ma.Email(required=True)
    password = ma.String(required=True)
    profile_pic = ma.String()
    active = ma.Boolean()

    todos = ma.Nested(TodoSchema, many=True)

    @validates('password')
    def validate_password(self, password):
        if len(password) < 5:
            raise ValidationError('Password min character is 5.')


user_schema = UserSchema()
user_schemas = UserSchema(many=True)


class LoginSchema(ma.Schema):
    email = ma.Email(required=True)
    password = ma.String(required=True)


login_schema = LoginSchema()


class UserBioSchema(ma.Schema):
    bio = ma.String()
    location = ma.String()
    website = ma.String()


user_bio_schema = UserBioSchema()


class UserEmailSchema(ma.Schema):
    email = ma.Email(required=True)


user_email_schema = UserEmailSchema()


class UserPasswordChangeSchema(ma.Schema):
    email = ma.Email(required=True)
    password = ma.String(required=True)


user_password_change_schema = UserPasswordChangeSchema()
