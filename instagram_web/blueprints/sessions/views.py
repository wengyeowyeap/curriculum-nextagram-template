import os
import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from werkzeug.security import check_password_hash

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/sign_in', methods=['GET'])
def sign_in_page():
    return render_template('sessions/sign_in.html')


@sessions_blueprint.route('/', methods=['POST'])
def sign_in():
  username = request.form.get('username')
  print(username)
  password_to_check = request.form['password'] # password keyed in by the user in the sign in form
  user_exist = User.get_or_none(User.username == username)
  if user_exist:
    hashed_password = user_exist.password_hash # password hash stored in database for a specific user
    print(hashed_password)
    pw_match = check_password_hash(hashed_password, password_to_check) # what is result? Test it in Flask shell and implement it in your view function!
    if pw_match:
      return redirect(url_for('users.show', username=username))
    if not pw_match:
      flash("Wrong Password")
      return redirect(url_for('sessions.sign_in_page'))
  if not user_exist:
    flash("User not exist")
    return redirect(url_for('sessions.sign_in_page'))

    
