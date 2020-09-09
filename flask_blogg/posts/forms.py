
from flask_wtf import FlaskForm
from wtforms import StringField , SubmitField 
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[
                          DataRequired()], widget=TextArea())
    submit = SubmitField('Post it')


class PostUpdateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[
                          DataRequired()], widget=TextArea())
    submit = SubmitField('Update it')

