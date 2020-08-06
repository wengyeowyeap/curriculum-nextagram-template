import os
import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from urllib.parse import urlparse, urljoin

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
    pw_match = check_password_hash(hashed_password, password_to_check) # what is result? Test it in Flask shell and implement it in your view function!
    if pw_match:
      login_user(user_exist)
      flash('Logged in successfully.')
      return redirect(url_for('users.show', username=user_exist.username))
    if not pw_match:
      flash("Wrong Password")
      return redirect(url_for('sessions.new'))
  if not user_exist:
    flash("User not exist")
    return redirect(url_for('sessions.new'))

@sessions_blueprint.route('/delete', methods=['POST'])
@login_required
def destroy():
    # remove user info from browser session
    # session.pop('user_id', None)
    logout_user()
    flash("Logout success!","primary")
    return redirect(url_for("sessions.new"))