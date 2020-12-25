import os
from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Post
from slugify import slugify

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


class PostCreateForm(FlaskForm):
    title = StringField('Titulo', validators=[DataRequired(), Length(6, 120)])
    pagedown = PageDownField('Contenido', validators=[DataRequired()])
    upload = FileField('Imagen', validators=[
        FileAllowed(ALLOWED_EXTENSIONS)])
    submit = SubmitField('Publicar Post')

    def validate_title(self, title):
        t = title.data.strip()
        post = Post.query.filter_by(title=t).first()
        if post:
            raise ValidationError(
                'Este post con este nombre ya existe, por favor intenta con otro.')

    def validate_slug(self, title):
        slug = slugify(title.data.strip())
        post = Post.query.filter_by(slug=slug).first()
        if post:
            raise ValidationError(
                'Este post con este nombre ya existe, por favor intenta con otro.')


class CommentForm(FlaskForm):
    body = TextAreaField('Mi comentario', validators=[DataRequired()])
    submit = SubmitField('Comentar')
