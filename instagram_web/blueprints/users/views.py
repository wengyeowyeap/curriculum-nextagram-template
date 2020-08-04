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
    hashed_password = generate_password_hash(password) # store this in database
    
    if User.create(username = username, password = hashed_password, email = email):
        flash("Successfully saved.")
        return redirect(url_for('users.show', username=username))
    else:
        print('ERROR, did not create record.')
        return render_template('users/new.html')

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    return '<h1>Added New User!</h1>'


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
