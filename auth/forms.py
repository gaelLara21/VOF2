from os import access
from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, RadioField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email,  EqualTo
from home.views import home_blueprint

class LoginForm(FlaskForm):
    email = EmailField('Username', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class RegisterForm(FlaskForm):
    regname = StringField('Nombre')
    reglastname = StringField('Apellidos')
    regemail = EmailField('Username')
    regpassword = PasswordField('Contraseña')
    regreppassword = PasswordField('Reppaswsword')
    submit = SubmitField('Registrate')