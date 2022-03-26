#contact/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Email


class ContactUserForm(FlaskForm):
    username = StringField('UserName',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    title = StringField('Title',validators=[DataRequired()])
    text= TextAreaField('お問合せ内容',validators=[DataRequired()])
    submit = SubmitField('Send')