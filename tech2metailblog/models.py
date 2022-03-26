#models.py
from datetime import datetime
import pytz
from tech2metailblog import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = "users"
    
    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(20),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    
    posts = db.relationship('BlogPost',backref='author',lazy=True)
    
    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def __repr__(self):
        return f"username: {self.username}"
    
class BlogPost(db.Model):
    
    users = db.relationship(User)
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    
    date = db.Column(db.DateTime,nullable=False,default=datetime.now(pytz.timezone('Asia/Tokyo')))
    title = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text,nullable=False)
    
    def __init__(self,title,text,user_id):
        self.title = title
        self.text = text
        self.user_id = user_id
        
    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} --- {self.title}"
    

class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50),unique=True, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    published_by = db.Column(db.String(50), nullable=False)
    published_at = db.Column(db.Integer, nullable=False)
    img_link = db.Column(db.String(100))
    pur_link = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)
    
    def __init__(self, title=None, author=None, 
                 published_by=None, published_at=None, img_link=None, pur_link=None):
        self.title = title
        self.author = author
        self.published_by = published_by
        self.published_at = published_at
        self.img_link = img_link
        self.pur_link = pur_link
        self.created_at = datetime.now(pytz.timezone('Asia/Tokyo'))
        
    def __repr__(self):
        return '<Books id:{} title:{} author:{} published_by:{}>'.format(self.id, self.title, self.author, self.published_by)
    
    
class Contact(db.Model):
    __tablename__ = "contact"
    
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),nullable=False,index=True)
    email = db.Column(db.String(64),nullable=False, index=True)
    title = db.Column(db.String(64),nullable=False)
    text = db.Column(db.Text,nullable=False)
    
    def __init__(self,email,username,title,text):
        self.email = email
        self.username = username
        self.title = title
        self.text = text
    
    def __repr__(self):
        return f"username: {self.username} email: {self.email} title: {self.title} text: {self.text}"