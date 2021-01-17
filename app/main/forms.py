from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length


class SendEmailForm(FlaskForm):
    title = StringField('title', validators=[
                        DataRequired(), Length(min=5, max=11)])
    body = TextAreaField('body', validators=[DataRequired()])
    submit = SubmitField('Enviar mensaje')

    def validate_title(self, title):
        if title is None:
            raise ValidationError('El Campo no debe de ser vacío')
