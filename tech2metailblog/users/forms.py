from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from tech2metailblog.models import User

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log In')
    
class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('UserName',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='パスワードが違います。')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Emailアドレスは既に登録されています。')
        
    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('ユーザーネームは既に登録されています。')

class UpdateUserForm(FlaskForm):
    
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('UserName',validators=[DataRequired()])
    #password = PasswordField('Password',validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')
    
    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Emailアドレスは既に登録されています。')
        
    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('ユーザーネームは既に登録されています。')
        
