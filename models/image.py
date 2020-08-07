from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property

class Image(BaseModel):
  user = pw.ForeignKeyField(User, backref="image", on_delete="CASCADE")
  image_path = pw.TextField(null=True)
  
  @hybrid_property
  def full_image_path(self):
      if self.image_path:
          from app import app
          return app.config.get("S3_LOCATION") + self.image_path
      else:
          return ""