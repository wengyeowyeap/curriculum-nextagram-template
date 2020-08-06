import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models.user import User
from flask_login import login_required, login_user

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
def edit(id):
    pass

@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
