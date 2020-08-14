from flask import Blueprint
from flask import jsonify, request
from models.image import Image
from flask_jwt_extended import jwt_required, get_jwt_identity

images_api_blueprint = Blueprint('images_api',
                             __name__,
                             template_folder='templates')

@images_api_blueprint.route('/', methods=['GET'])
def get_all_image():
  all_image_list = []
  for i in Image.select():
    image = {
        "id" : i.id,
        "url": i.full_image_path
    }
    all_image_list.append(image)
  return jsonify(all_image_list)

@images_api_blueprint.route('/<id>', methods=['GET'])
def get_image(id):
    response = []
    find_user = Image.get_or_none(Image.user_id == id)
    if find_user:
      for i in Image.select().where(Image.user_id == id):
        image = {
            "id" : i.id,
            "url": i.full_image_path
        }
        response.append(image)
    else:
      error = {
            "message": "User does not exist",
            "status": "failed"
      }
      response.append(error)
    return jsonify(response)

@images_api_blueprint.route('/me', methods=['GET'])
@jwt_required
def me():
    online_user = get_jwt_identity()
    response = []
    for i in Image.select().where(User.id == online_user['id']):
        image = i.full_image_path
        response.append(image)
    return jsonify(response)