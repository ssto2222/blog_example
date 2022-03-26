#tech2metailblog/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY']="mysecret"
app.config['WTF_CSRF_SECRET_KEY']="a csrf secret key"



#######################################
###         Database Setup #############
############################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
Migrate(app,db)

#######################################
#### Upload files
app.config['UPLOAD_FOLDER'] = os.path.join(basedir,'static','uploads')

###################################
### LOGIN CONFIGS
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'
########################################

from tech2metailblog.blog_posts.views import blog_posts
app.register_blueprint(blog_posts)

from tech2metailblog.contacts.views import contacts
app.register_blueprint(contacts)

from tech2metailblog.core.views import core
app.register_blueprint(core)

from tech2metailblog.error_pages.handlers import error_pages
app.register_blueprint(error_pages)

from tech2metailblog.users.views import users
app.register_blueprint(users)

from tech2metailblog.books.views import books
app.register_blueprint(books)



