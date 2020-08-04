from models.base_model import BaseModel
import peewee as pw

class User(BaseModel):
    username = pw.CharField(unique=True)
    password = pw.CharField()
    email = pw.CharField(unique=True)

    def validate(self):
        username_duplicate = User.get_or_none(User.username == self.username)
        email_duplicate = User.get_or_none(User.email == self.email)

        if username_duplicate and email_duplicate:
            self.errors.append('Username and email has been used')
        elif username_duplicate:
            self.errors.append('Username has been used')
        elif email_duplicate:
            self.errors.append('Email has been used')
