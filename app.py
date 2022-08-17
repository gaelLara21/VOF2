### importsde flask y python ###
from email.headerregistry import ContentTransferEncodingHeader
from os import access
from flask import Flask, render_template, request, url_for, redirect, Blueprint,flash, Response,session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, RadioField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email,  EqualTo
from flask_login import LoginManager

### imports apps blueprints ###
from home.views import home_blueprint, productos
from auth.views import auth_blueprint
from error_pages.handlers import error_pages_blueprint
from auth.models import get_user_by_id, get_user_by_username_and_password
from flaskext.mysql import MySQL


## app de flask ##
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['ENV'] = 'development'

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456789'
app.config['MYSQL_DATABASE_DB'] = 'mydb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


mysql = MySQL()
mysql.init_app(app)

#### Configuracion de Flask Login ####
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@app.route('/indexcliente')
def indexcliente():
    return render_template('indexcliente.html')

@app.route('/logincliente')
def logincliente():
    return render_template('logincliente.html')

@app.route('/logincli', methods=['GET', 'POST'])
def logincli():
    if request.method == 'POST':

        # and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM clientes WHERE username = %s AND password = %s',
                    (username, password))
        print(username,password)
        # print(username)
        # print(password)
        account = cur.fetchone()
        conn.commit()

        if account:

            session['loggedin'] = True
            session['username'] = username
            session['password'] = password

            return render_template('indexcliente.html')

        else:

            return render_template('logincliente.html')

    return render_template('logincliente.html')


@app.route('/login2', methods=['GET', 'POST'])
def login2():
    msg = ''
    if request.method == 'POST':
        # and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM user WHERE username = %s AND password = %s',
                    (username, password))

        # print(username)
        # print(password)
        account = cur.fetchone()
        conn.commit()

        if account:

            session['loggedin'] = True
            session['username'] = username
            session['password'] = password

            return redirect(url_for('vista.html'))

        else:

            msg = 'Contraseña y/o Usuario Incorrecto'

    return render_template('login2.html', msg=msg)

@app.route('/registrarcliente', methods=['GET', 'POST'])
def registrarcliente():
    return render_template('registrarcliente.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':

        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        username = request.form['username']
        password = request.form['password']

        username = request.form['username']
        password = request.form['password']

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute('select * from user where username=(%s) and password=(%s)',
                    (username, password))
        user = cur.fetchone()

        if user:

            cur.execute('insert into user values (%s,%s,%s,%s)',
                        (nombre, apellidos, username, password))
            conn.commit()
            flash('Usuario registrado')

        else:

            flash('Usuario del administrador incorrecto')

    return render_template('register.html')

@app.route('/productosadmi')
def productosadmi():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute('select * from productos order by idproductos desc')
    productos=cur.fetchall()

    return render_template('productosadmi.html', productos=productos)

@app.route('/productoscliente')
def productoscliente():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute('select * from productos order by idproductos desc')
    productos=cur.fetchall()

    return render_template('productoscliente.html', productos=productos)

@app.route('/addproducto')
def addproducto():
    return render_template('addproducto.html')

@app.route('/addproducto.html', methods=['POST'])
def anadirproducto():
    if request.method == 'POST':
        #identificador= request.form['identificador']
        imagen = request.form['imagen']
        nombreproducto = request.form['nombreproducto']
        material = request.form['material']
        precio = request.form['precio']

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute('select idproductos from productos order by idproductos desc')
        AI=cur.fetchone()
        AICHIDO=AI[0]
        print(AICHIDO)
        AICHIDOCHIDO=AICHIDO+1

        cur.execute('insert into productos (idproductos,imagen,nombreproducto,material,precio) values (%s,%s,%s,%s,%s)',
        (AICHIDOCHIDO,imagen,nombreproducto,material,precio))
        conn.commit()
    return render_template('addproducto.html')


@app.route('/eliminar_pro/<string:iden>')
def eliminar_pro(iden):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute('delete from productos where (idproductos)=(%s)',
                (iden))
    conn.commit()

    cur.execute('ALTER TABLE productos AUTO_INCREMENT=1')
    conn.commit()

    cur.execute('select * from productos order by idproductos desc')
    productos=cur.fetchall()

    return render_template('productosadmi.html', productos=productos)

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

######Panel De Admin#######
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin', methods=['GET', 'POST'])
def loginad():
    if request.method == 'POST':

        # and 'username' in request.form and 'password' in request.form:
        user = request.form['user']
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM user WHERE  user= %s AND username = %s AND password = %s',
                    (user, username, password))
        print(user,username,password)
        # print(username)
        # print(password)
        account = cur.fetchone()
        conn.commit()

        if account:

            session['loggedin'] = True
            session['user'] = user
            session['username'] = username
            session['password'] = password

            return render_template('vista.html')

        else:

            return render_template('admin.html')

    return render_template('admin.html')

@app.route('/vista')
def vista():
   return render_template('vista.html')

######Datos de envio#######

@app.route('/Confirmacion')
def confirmacion():
    return render_template('Confirmacion.html')

 
####### registro de apps #######
app.register_blueprint(home_blueprint)
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(error_pages_blueprint)

if  __name__ == '__main__':
    app.run(debug=True)

    