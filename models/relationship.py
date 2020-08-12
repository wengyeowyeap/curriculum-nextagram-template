from models.base_model import BaseModel
import peewee as pw
from models.user import User

class Relationship(BaseModel):
  following = pw.ForeignKeyField(User, backref='following', on_delete="CASCADE")
  followed = pw.ForeignKeyField(User, backref='followed', on_delete="CASCADE")
  pending = pw.BooleanField(default=False)