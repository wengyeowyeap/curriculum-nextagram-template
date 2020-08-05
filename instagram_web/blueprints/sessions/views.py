import os
import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from werkzeug.security import check_password_hash

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
  username = request.form.get('username')
  password_to_check = request.form['password'] # password keyed in by the user in the sign in form
  user_exist = User.get_or_none(User.username == username)
  if user_exist:
    hashed_password = user_exist.password_hash # password hash stored in database for a specific user
    print(hashed_password)
    pw_match = check_password_hash(hashed_password, password_to_check) # what is result? Test it in Flask shell and implement it in your view function!
    if pw_match:
      session["user_id"] = user_exist.id
      return redirect(url_for('users.show', username=username))
    if not pw_match:
      flash("Wrong Password")
      return redirect(url_for('sessions.new'))
  if not user_exist:
    flash("User not exist")
    return redirect(url_for('sessions.new'))

@sessions_blueprint.route('/')
def destroy():
  session.pop('user_id', None)
  flash("Signed out successfully!")
  return redirect(url_for('sessions.new'))