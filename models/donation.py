from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.image import Image

class Donation(BaseModel):
  user = pw.ForeignKeyField(User, backref="donation", on_delete="CASCADE")
  image = pw.ForeignKeyField(User, backref="donation", on_delete="CASCADE")
  amount = pw.IntegerField(null=False, default=0) #last two number stored is decimal