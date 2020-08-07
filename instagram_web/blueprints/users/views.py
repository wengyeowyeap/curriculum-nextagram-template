from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models.user import User
from flask_login import login_required, login_user, current_user
from instagram_web.util.helpers import upload_file_to_s3
from werkzeug.security import check_password_hash
from werkzeug import secure_filename

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    new_user = User(username = username, password = password, email = email)

    if new_user.save():
        flash("Successfully signed up!", "success")
        login_user(new_user)
        return redirect(url_for('users.show', username=username))
    else:
        for error in new_user.errors:
            flash(error, "danger")
        return redirect(url_for('users.new'))

@users_blueprint.route('/<username>', methods=["GET"])
@login_required 
def show(username):
    user = User.get_or_none(User.username == username)
    if user:
        return render_template('users/show.html', username=username, user=user)
    else:
        return abort(404)
        
@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"

@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required 
def edit(id):
    user = User.get_or_none(User.id== id)
    if user:
        if current_user.id == int(id):
            return render_template("users/edit.html", user=user)
        else:
            return abort(403)
    else:
        return abort(404)

@users_blueprint.route('/<id>', methods=['POST'])
@login_required 
def update(id):
    user = User.get_or_none(User.id == id)
    if user:
        if current_user.id == int(id):
            current_pw = request.form['current_password']
            hashed_password = current_user.password_hash
            pw_match = check_password_hash(hashed_password, current_pw)
            if pw_match:
                form_type = request.form.get('form_type')
                if form_type == 'username':        
                    user.username = request.form.get('new_username')
                    message="Username Changed!"
                if form_type == 'password':
                    user.password = request.form.get('new_password')
                    message="Password Changed!"
                if form_type == 'email':
                    user.email = request.form.get('new_email')
                    message="Email Changed!"

                if user.save():
                    flash(message)
                    return redirect(url_for('users.show', username=user.username))
                else:
                    for error in user.errors:
                        flash(error, "danger")
                    return redirect(url_for('users.edit', id = id))
            else:
                flash("Wrong Password!", "danger")
                return redirect(url_for('users.edit', id = id))
        else:
            return abort(403)
    else:
        return abort(404)

@users_blueprint.route('/<id>/upload', methods=['POST'])
@login_required
def upload_profile(id):
    user = User.get_or_none(User.id == id)
    if user:
        if current_user.id == int(id):
            # Upload image
            if "profile_image" not in request.files:
                flash("No file provided!")
                return redirect(url_for("users.edit", id = id))

            file = request.files["profile_image"]
            if 'image' not in file.mimetype:
                flash("Please upload an image!")
                return redirect(url_for("users.edit", id = current_user.id))
            else:
                file_extension = file.mimetype
                file_extension = file_extension.replace('image/', '.')
            
            file.filename = user.username + "_profile_image" + file_extension
            file.filename = secure_filename(file.filename)
            # Get path to image on s3 bucket
            image_path = upload_file_to_s3(file,user.username)
            # Update user with image path
            user.image_path = image_path
            if user.save():
                return redirect(url_for("users.show", username=user.username))
            else:
                flash("Could not upload image. Please try again")
                return redirect(url_for("users.edit", id=id)) 
            return redirect(url_for('users.show', username=user.username))
        else:
            return abort(403)
    else:
        return abort(404)