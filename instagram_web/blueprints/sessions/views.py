import os
import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from werkzeug.security import generate_password_hash

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


