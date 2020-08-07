import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models.user import User
from models.image import Image
from flask_login import login_required, current_user
from instagram_web.util.helpers import upload_file_to_s3
from werkzeug import secure_filename
from datetime import datetime

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('images/new.html')

@images_blueprint.route('/', methods=['POST'])
@login_required
def create():
  user = User.get_or_none(User.id == current_user.id)
  if user:
    # Upload image
    if "new_image" not in request.files:
      flash("No file provided!")
      return redirect(url_for("images.new"))

    file = request.files["new_image"]
    if 'image' not in file.mimetype:
      flash("Please upload an image!")
      return redirect(url_for("images.new"))
    else:
      file_extension = file.mimetype
      file_extension = file_extension.replace('image/', '.')
    
    file.filename = str(datetime.now()) + file_extension
    file.filename = secure_filename(file.filename)
    image_path = upload_file_to_s3(file,user.username)
    image = Image(user_id = user.id, image_path = image_path)

    if image.save():
      flash("Successfully uploaded your new photo!", "success")
      return redirect(url_for("users.show", username=user.username))
    else:
      flash("Could not upload image. Please try again")
      return redirect(url_for("images.new")) 
    return redirect(url_for('users.show', username=user.username))
  else:
    return abort(404)
