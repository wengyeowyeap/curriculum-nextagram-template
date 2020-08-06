import os
import config
from flask import Flask, render_template
from models.base_model import db
from models.user import User
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
csrf = CSRFProtect(app)
app.secret_key = os.getenv('SECRET_KEY')
if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "sessions.new"   # if user try to access login_required route without sign in, will redirect to `sessions.new`
login_manager.login_message = "Please log in before proceeding"
login_manager.login_message_category = "warning"

@app.before_request
def before_request():
    db.connect()

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)

@app.errorhandler(400)
def bad_request(e):
    return render_template('error.html', code = 400), 400

@app.errorhandler(401)
def unauthorized(e):
    return render_template('error.html', code = 401), 401

@app.errorhandler(403)
def forbidden(e):
    return render_template('error.html', code = 403), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', code = 404), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', code = 500), 500
