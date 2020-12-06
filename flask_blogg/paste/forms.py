from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, ValidationError
from flask_blogg.models import Paste


class PasteForm(FlaskForm):
    title = StringField('Title', validators=[
                        DataRequired(), Length(min=4, max=100)])
    content = StringField('Content', validators=[
                          DataRequired()], widget=TextArea())
    submit = SubmitField('Post it')

    def validate_title(self, title):
        title = Paste.query.filter_by(title=title.data).first()
        if title:
            raise ValidationError('OOPS !. That title is taken.')
