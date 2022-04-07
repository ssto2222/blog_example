#books/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired

class BooksPostForm(FlaskForm): 
    title = StringField('Title',validators=[DataRequired()])
    author = StringField('Author',validators=[DataRequired()])
    published_by = StringField('Publisher',validators=[DataRequired()])
    published_at = StringField('Published_at',validators=[DataRequired()])
    img_link = StringField('img_link',validators=[DataRequired()])
    ecsite_link = StringField('ECsite_link',validators=[DataRequired()])
    text= TextAreaField('Text',validators=[DataRequired()])
    submit=SubmitField('Post')