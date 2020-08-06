import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models.user import User
from flask_login import login_required, login_user, current_user
from werkzeug.security import check_password_hash

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
    user_exist = User.get_or_none(User.username == username)
    if user_exist:
        return render_template('users/show.html', username=username)
    else:
        return abort(404)
        
@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"

@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required 
def edit(id):
    return render_template('users/edit.html', id = id)

@users_blueprint.route('/<id>', methods=['POST'])
@login_required 
def update(id):
    current_pw = request.form['current_password']
    hashed_password = current_user.password_hash
    pw_match = check_password_hash(hashed_password, current_pw)
    if pw_match:
        form_type = request.form.get('form_type')
        user = User.get_or_none(User.id == id)
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

