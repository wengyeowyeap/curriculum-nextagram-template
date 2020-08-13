from models.base_model import BaseModel
import peewee as pw
import re
from playhouse.hybrid import hybrid_property
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password_hash = pw.TextField(null=False)
    password = None
    image_path = pw.TextField(null=True)
    private = pw.BooleanField(null=False, default=False)
    
    @hybrid_property
    def full_image_path(self):
        if self.image_path:
            from app import app
            return app.config.get("S3_LOCATION") + self.image_path
        else:
            return ""

    def validate(self):
        username_duplicate = User.get_or_none(User.username == self.username)
        email_duplicate = User.get_or_none(User.email == self.email)

        if username_duplicate and email_duplicate and username_duplicate.id != self.id and email_duplicate.id != self.id:
            self.errors.append('Username and email has been used')
        elif username_duplicate and username_duplicate.id != self.id:
            self.errors.append('Username has been used')
        elif email_duplicate and email_duplicate.id != self.id:
            self.errors.append('Email has been used')
        
        if self.password:
            if (len(self.password) < 6) or (re.search('[A-Z]',self.password) is None) or (re.search('[a-z]',self.password) is None) or (re.search('[0-9]',self.password) is None) or (re.search('[!@#$%]',self.password) is None):
                self.errors.append('Password requirement: 6 or more characters, uppercase letters, lowercase letters, numbers, special characters(!@#$%).')
            else:
                self.password_hash = generate_password_hash(self.password) # store this in database    

    def follow(self, target_user):
        from models.relationship import Relationship
        if target_user.private:
            new_r = Relationship(following_id = self.id, followed_id = target_user.id, pending = True)
        else:
            new_r = Relationship(following_id = self.id, followed_id = target_user.id, pending = False)
        return new_r.save()

    def unfollow(self, target_user):
        from models.relationship import Relationship
        r = Relationship.get_or_none(followed=target_user, following=self)
        return r.delete_instance()
            
    def approval(self, target_user, approval):
        from models.relationship import Relationship
        if approval == 'approve':
            r = Relationship.get_or_none(followed=self, following=target_user)
            r.pending = False
            r.save()
            return True
        else:
            r = Relationship.get_or_none(followed=self, following=target_user)
            r.delete_instance()
            return False

    def follow_status(self, target_user):
        from models.relationship import Relationship
        search_r = Relationship.get_or_none(followed=target_user, following=self)
        return search_r
    
    @hybrid_property
    def pending_follower(self):
        from models.relationship import Relationship
        p_follower_list = Relationship.select(Relationship.following).where(Relationship.followed == self, Relationship.pending == True)
        return p_follower_list
    
    @hybrid_property
    def pending_request(self):
        from models.relationship import Relationship
        p_following_list = Relationship.select(Relationship.followed).where(Relationship.following == self, Relationship.pending == True)
        return p_following_list

    @hybrid_property
    def follower(self):
        from models.relationship import Relationship
        my_follower = Relationship.select(Relationship.following).where(Relationship.followed == self, Relationship.pending == False)
        return my_follower
    
    @hybrid_property
    def follower_total(self):
        from models.relationship import Relationship
        my_follower = Relationship.select(Relationship.following).where(Relationship.followed == self, Relationship.pending == False)
        return len(my_follower)
    
    @hybrid_property
    def following(self):
        from models.relationship import Relationship
        im_following = Relationship.select(Relationship.followed).where(Relationship.following == self, Relationship.pending == False)
        return im_following

    @hybrid_property
    def following_total(self):
        from models.relationship import Relationship
        im_following = Relationship.select(Relationship.followed).where(Relationship.following == self, Relationship.pending == False)
        return len(im_following)
    
    @hybrid_property
    def image_feed(self):
        from models.relationship import Relationship
        from models.image import Image
        images = Image.select().join(Relationship, on = (Image.user_id == Relationship.followed)).where(Relationship.following == self, Relationship.pending == False)
        return images

