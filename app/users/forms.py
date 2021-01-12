from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from wtforms.fields.html5 import EmailField
from ..models import User

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

    def validate_email(self, field):
        email = User.query.filter_by(email=field.data).first()
        if email:
            raise ValidationError('Este email ya existe.')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(
        "Por favor vuelva a ingresar su email."), Email('Por favor Ingrese un email Correcto.')])
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


class EmailResetPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[Email(),  DataRequired()])
    submit = SubmitField('Enviar')

    def validate_email(self, field):
        email = User.query.filter_by(email=field.data).first()

        if not email:
            raise ValidationError(
                'El correo ingresado no se encuentra registrado')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(
        min=6, max=30, message="Por favot revise lo errores"),  EqualTo('password_repeat', message="Las contraseñas deben de ser iguales")])
    password_repeat = PasswordField('Confirme su Contraseña', validators=[DataRequired(), Length(
        min=6, max=30, message="Por favot revise lo errores")])

    submit = SubmitField('Reestablecer mi contraseña')

    def validate_password(self, field):

        if field.data != self.password_repeat.data:
            raise ValidationError(
                'Las contraseñas ingresadas no son iguales, intente nuevamente')
