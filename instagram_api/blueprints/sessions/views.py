from flask import Blueprint
from flask import jsonify, request
from models.user import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

sessions_api_blueprint = Blueprint('sessions_api',
                             __name__,
                             template_folder='templates')

@sessions_api_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.get_or_none(User.username == username)

    error = {
    "message": "Some error occurred. Please try again.",
    "status": "fail"
    }

    if user:
        hashed_password = user.password_hash # password hash stored in database for a specific user
        pw_match = check_password_hash(hashed_password, password) # what is result? Test it in Flask shell and implement it in your view function!
        if pw_match:
            identity = {
                'id': user.id,
                "username": user.username,
            }
            jwt = create_access_token(identity=identity)
            success = {
                "auth_token": jwt,
                "message": "Successfully signed in.",
                "status": "success",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "profile_picture": user.full_image_path
                }
            }
            return jsonify(success)
        if not pw_match:
            return jsonify(error)
    if not user:
        return jsonify(error)
