from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from app.models import User

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[
                           DataRequired("Este Campo es requerido."), Length(4, 40)])
    email = StringField('Email', validators=[DataRequired("Este Campo es requerido."), Email(
        "Este Email no es valido."), Length(min=10, message="El Email como minimo debera tener 10 caracteres.")])
    password = PasswordField('Contraseña', validators=[DataRequired(
        "Este Campo es requerido."), EqualTo('password_conf', "La contraseña ingresada no son iguales")])
    password_conf = PasswordField('Confirma tu contraseña', validators=[DataRequired(
        "Este Campo es requerido."), EqualTo('password', "Por favor intente ingresar nuevamente la contraseña.")])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.strip()).first()
        if user:
            raise ValidationError('Este nombre de usuario ya existe.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email es incorrecto.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(
        "Por favor vuelva a ingresar su email.")])
    password = PasswordField('Contraseña', validators=[DataRequired(
        "Por favor intente inrgesar una contraseña correcta.")])
    remember = BooleanField('Recordarme', default=False)
    submit = SubmitField('Ingresar')

    def validate_username(self, password):
        user = User.query.filter_by(password=password.data.strip()).first()
        if user:
            raise ValidationError(
                'Por favor intenta nuevamente poner tu contraseña.')


class AccountForm(FlaskForm):
    email = StringField('Email', validators=[
                        DataRequired(), Email("Este email es incorrecto.")])
    username = StringField('Nombre de usuario', validators=[
                           DataRequired(), Length(4, 40)])
    name = StringField('Nombre', validators=[Length(0, 60)])
    address = StringField('Dirección', validators=[Length(0, 60)])
    upload = FileField('Imagen para mi perfil', validators=[
                       FileAllowed(ALLOWED_EXTENSIONS)])
    submit = SubmitField('Actualizar')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data.strip()).first()
            if user:
                raise ValidationError('Este nombre de usuario ya existe.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data.strip()).first()
            if user:
                raise ValidationError('Este email es incorrecto.')
