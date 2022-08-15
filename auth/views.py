from os import access
from flask import Flask, render_template, request, url_for, redirect, Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, RadioField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email,  EqualTo
from home.views import home_blueprint

##### import forms #####
from.forms import LoginForm, RegisterForm
from auth.models import get_user_by_id, get_user_by_username_and_password

auth_blueprint = Blueprint('auth', __name__)
@auth_blueprint.route('/auth/login', methods=['GET', 'POST'] )
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data 

        user = get_user_by_username_and_password(email, password)


        return render_template('admin/index.html', email=email)
    
    
    return render_template('/auth/login.html', form=form)

@auth_blueprint.route('/auth/signin', methods=['GET', 'POST'] )
def signin():
    form = RegisterForm()

    if form.validate_on_submit():
        regname = form.regname.data
        reglastname = form.reglastname.data
        regcorreo = form.regcorreo.data
        regpassword = form.regpassword.data
        regreppassword = form.regreppassword.data


        return render_template('admin/index.html', regname=regname, reglastname=reglastname, regcorreo=regcorreo)

    
    return render_template('/auth/signin.html', form=form)

@auth_blueprint.route('/Welcome', methods=['GET', 'POST'])
def Welcome(form):

    
    form = LoginForm()
    

    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data
       
        return render_template('admin/index.html', email=email)
    return render_template('auth/formulario.html'), redirect(url_for('login'))
