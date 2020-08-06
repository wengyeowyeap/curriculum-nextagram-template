from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password_hash = pw.TextField(null=False)
    password = None

    def validate(self):
        username_duplicate = User.get_or_none(User.username == self.username)
        email_duplicate = User.get_or_none(User.email == self.email)

        if username_duplicate and email_duplicate:
            self.errors.append('Username and email has been used')
        elif username_duplicate:
            self.errors.append('Username has been used')
        elif email_duplicate:
            self.errors.append('Email has been used')
        
        if (len(self.password) < 6) or (re.search('[A-Z]',self.password) is None) or (re.search('[a-z]',self.password) is None) or (re.search('[0-9]',self.password) is None) or (re.search('[!@#$%]',self.password) is None):
            self.errors.append('Password requirement: 6 or more characters, uppercase letters, lowercase letters, numbers, special characters(!@#$%).')
        else:
            self.password_hash = generate_password_hash(self.password) # store this in database    
        
