from flask import Blueprint
from flask import jsonify, abort, request
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def get_all_user():
    response = []
    for u in User.select().order_by(User.id):
        user = {
            "id" : u.id,
            "username" : u.username,
            "email" : u.email,
            "profile_pic": u.full_image_path, 
        }
        response.append(user)

    return jsonify(response)

@users_api_blueprint.route('/<id>', methods=['GET'])
def get_user(id):
    find_user = User.get_or_none(User.id == id)
    if find_user:
      for i in User.select().where(User.id == id):
        response = {
            "id": id,
            "profileImage": i.full_image_path,
            "username": i.username
        }
    else:
        response = {
            "message": "User does not exist",
            "status": "failed"
        }
    return jsonify(response)

@users_api_blueprint.route('/me', methods=['GET'])
@jwt_required
def me():
    online_user = get_jwt_identity()
    for u in User.select().where(User.id == online_user['id']):
        response = {
            "email": u.email,
            "id": u.id,
            "profile_picture": u.full_image_path,
            "username": u.username
        }
    return jsonify(response)

@users_api_blueprint.route('/check_name', methods=['GET'])
def check_name():
    input = request.args.get("username")
    find_user = User.get_or_none(User.username == input)
    if find_user:
        response = {
            "exists": True,
            "valid": False
        }
    else:
        response = {
            "exists": False,
            "valid": True
        }
    return jsonify(response)

@users_api_blueprint.route('/check_email', methods=['GET'])
def check_email():
    input = request.args.get("email")
    find_email = User.get_or_none(User.email == input)
    if find_email:
        response = {
            "exists": True,
            "valid": False
        }
    else:
        response = {
            "exists": False,
            "valid": True
        }
    return jsonify(response)

@users_api_blueprint.route('/sign_up', methods=['POST'])
def sign_up():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    new_user = User(username = username, password = password, email = email)

    if new_user.save():
        identity = {
            'id': new_user.id,
            "username": new_user.username
        }
        jwt = create_access_token(identity=identity)
        response = {
            "auth_token": jwt,
            "message": "Successfully created a user.",
            "status": "success",
            "user": {
                "id": new_user.id,
                "profile_picture": "http://next-curriculum-instagram.s3.amazonaws.com/profile-placeholder.jpg",
                "username": new_user.username
            }
        }
    else:
        response = {
            "message": "Some error occured, please try again",
            "status": "failed"
        }
    return jsonify(response)
