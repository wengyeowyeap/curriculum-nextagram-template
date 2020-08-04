import os
import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from werkzeug.security import generate_password_hash

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

    if (len(password) < 6) or (re.search('[A-Z]',password) is None) or (re.search('[a-z]',password) is None) or (re.search('[0-9]',password) is None) or (re.search('[!@#$%]',password) is None):
        flash('Password requirement: 6 or more characters, uppercase letters, lowercase letters, numbers, special characters(!@#$%).')
        return render_template('users/new.html')
    else:
        hashed_password = generate_password_hash(password) # store this in database    
        new_user = User(username = username, password = hashed_password, email = email)
        if new_user.save():
            flash("Successfully signed up!")
            return redirect(url_for('users.show', username=username))
        else:
            for error in new_user.errors:
                flash(error)
            return render_template('users/new.html')

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    return render_template('users/show.html', username=username)


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
