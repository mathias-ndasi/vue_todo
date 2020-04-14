from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError

from app import models, db
from app.config import Config
from app.utils import util, email
from app.schemas import schema_user
from app.auth import token, decorators

account = Blueprint('account', __name__, url_prefix='/account')


@account.route('/signup', methods=['POST'])
def signup():
    error = None
    message = None
    success = False
    results = None

    data = request.get_json()

    if not data:
        error = {'email': 'Json data is required'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    try:
        clean_data = schema_user.user_schema.load(data)

        user = models.User.query.filter_by(email=clean_data['email']).first()

        if user:
            error = {'email': 'User already exist'}
            return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

        password = clean_data['password']
        hash_pwd = util.hash_password(password)

        new_user = models.User(
            first_name=clean_data.get('first_name', None), last_name=clean_data.get('last_name', None), email=clean_data.get('email', None), password=hash_pwd)
        email.account_comfirmation_email(new_user)

        success = True
        message = 'Account activation code sent to your email'

        return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('CREATED')

    except ValidationError as e:
        error = e.normalized_messages()

    return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')


@account.route('/account_confirmation', methods=['PUT'])
def account_confirm():
    error = None
    message = None
    success = False
    results = None

    try:
        data = request.get_json()

        if not data:
            error = {'secret_code': 'Json data is missen'}
            return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    except Exception as e:
        error = {'secret_code': 'Json data is missen'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    if not data:
        error = {'secret_code': 'This is a required field'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    secret_code = data['secret_code']

    user = models.User.query.filter_by(
        secret_code=secret_code, active=False).first()

    if not user:
        error = {'secret_code': 'Invalid secret code or user already activated'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    user.active = True
    user.secret_code = None
    db.session.commit()
    message = 'User account is activated, you can now login'
    success = True

    return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('SUCCESS')


@account.route('/login', methods=['POST'])
def login():
    error = None
    message = None
    success = False
    results = None

    if request.is_json:
        try:
            data = request.get_json()

            if not data:
                error = {'email': 'Json data is missen'}
                return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error = {'email': 'Json data is missen'}
            return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            clean_data = schema_user.login_schema.load(data)

            user = models.User.query.filter_by(
                email=clean_data['email'], active=True, secret_code=None).first()

            if not user:
                error = {'email': 'User not found'}
                return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

            if not util.verify_password(user, clean_data['password']):
                error = {'password': 'Incorrect password'}
                return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

            user_token = token.generate_token(user)
            message = 'User successfully login'
            success = True
            results = schema_user.user_schema.dump(user)
            results['token'] = user_token

            return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('SUCCESS')

        except ValidationError as e:
            error = e.normalized_messages()
    else:
        error = {'email': "Json data is required"}

    return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')


@account.route('/user/<string:public_id>', methods=['GET'])
@decorators.token_required
def get_single_user(public_id):
    error = None
    message = None
    success = False
    results = None

    user = models.User.query.filter_by(
        public_id=public_id, active=True, secret_code=None).first()

    if not user:
        error = 'User not found'
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    success = True
    results = schema_user.user_schema.dump(user)

    return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('SUCCESS')


@account.route('/users', methods=['GET'])
@decorators.token_required
def get_all_users():
    error = None
    message = None
    success = False
    results = None

    users = models.User.query.filter_by(
        active=True, secret_code=None).all()

    if not users:
        error = 'User not found'
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    success = True
    results = schema_user.user_schemas.dump(users)

    return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('SUCCESS')


@account.route('/<string:public_id>/profile_pic', methods=['PUT'])
@decorators.token_required
def update_profile_pic(public_id):
    error = None
    message = None
    success = False
    results = None

    if not request.files:
        error = {'server': 'Form data is required'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    if len(request.files) > 1:
        error = {'profile_pic': 'Only a single image can be updated'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    if not request.files.get('profile_pic', None):
        error = {'profile_pic': 'This is a required field'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    user = models.User.query.filter_by(
        public_id=public_id, active=True, secret_code=None).first()

    if not user:
        error = {'server': 'Invalid user'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    file = request.files['profile_pic']
    picture_path = util.save_picture(file, user)

    if picture_path == None:
        error = {'profile_pic': 'Invalid file extension'}
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    user.profile_pic = picture_path
    db.session.commit()

    success = True
    message = 'Profile pic successfully updated'
    results = schema_user.user_schema.dump(user)

    return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('SUCCESS')


@account.route('/delete/<string:public_id>', methods=['DELETE'])
@decorators.token_required
def delete_user(public_id):
    error = None
    message = None
    success = False
    results = None

    user = models.User.query.filter_by(
        public_id=public_id, active=True).first()

    if not user:
        error = 'User not found'
        return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

    user.active = False

    db.session.commit()

    success = True
    message = 'User successfully deleted'

    return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('NO_CONTENT')


@account.route('/user/update/<string:public_id>/bio', methods=['PUT'])
@decorators.token_required
def update_user_bio(public_id):
    error = None
    message = None
    success = False
    results = None

    if request.is_json:
        try:
            data = request.get_json()

            if not data:
                error = 'Json data is missen'
                return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error = 'Json data is missen'
            return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            clean_data = schema_user.user_bio_schema.load(data)

            user = models.User.query.filter_by(
                public_id=public_id, active=True, secret_code=None).first()

            if not user:
                error = 'User not found'
                return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

            if clean_data.get('bio'):
                user.bio = clean_data['bio']

            if clean_data.get('location'):
                user.location = clean_data['location']

            if clean_data.get('website'):
                user.website = clean_data['website']

            db.session.commit()

            message = 'User bio successfully updated'
            success = True
            results = schema_user.user_schema.dump(user)

            return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('SUCCESS')

        except ValidationError as e:
            error = e.normalized_messages()
    else:
        error = "Json data is required"

    return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')


@account.route('/password_reset', methods=['POST'])
def password_reset():
    error = None
    message = None
    success = False
    results = None

    if request.is_json:
        try:
            data = request.get_json()

            if not data:
                error = 'Json data is missen'
                return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error = 'Json data is missen'
            return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            clean_data = schema_user.user_email_schema.load(data)

            user = models.User.query.filter_by(
                email=clean_data['email'], active=True).first()

            if not user:
                error = 'User not found'
                return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

            email.password_reset_email(user)

            message = 'Check your email for password reset secret code'
            success = True

            return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('SUCCESS')

        except ValidationError as e:
            error = e.normalized_messages()
    else:
        error = "Json data is required"

    return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')


@account.route('/password_reset_code_validation', methods=['PUT'])
def password_reset_code_validation():
    error = None
    message = None
    success = False
    results = None

    if request.is_json:
        try:
            data = request.get_json()

            if not data:
                error = 'Json data is missen'
                return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error = 'Json data is missen'
            return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

        if not data.get('secret_code'):
            error = {'secret_code': 'This is a required field'}
            return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            user = models.User.query.filter_by(
                secret_code=data['secret_code'], active=True).first()
        except Exception as e:
            pass

        if not user:
            error = 'User not found'
            return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

        user.secret_code = None
        db.session.commit()

        message = 'Secret code valid'
        success = True
        results = schema_user.user_schema.dump(user)

        return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('SUCCESS')

    else:
        error = "Json data is required"

    return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')


@account.route('/password_reset_confirm', methods=['PUT'])
def password_reset_confirm():
    error = None
    message = None
    success = False
    results = None

    if request.is_json:
        try:
            data = request.get_json()

            if not data:
                error = 'Json data is missen'
                return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error = 'Json data is missen'
            return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            clean_data = schema_user.user_password_change_schema.load(data)

            user = models.User.query.filter_by(
                email=clean_data['email'], active=True).first()

            if not user:
                error = 'User not found'
                return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')

            user.password = util.hash_password(clean_data['password'])

            db.session.commit()

            message = 'User password successfully updated, you can now login'
            success = True

            return jsonify({'success': success, 'data': results, 'message': message}), util.http_status_code('SUCCESS')

        except ValidationError as e:
            error = e.normalized_messages()
    else:
        error = "Json data is required"

    return jsonify({'success': success, 'error': error}), util.http_status_code('BAD_REQUEST')
