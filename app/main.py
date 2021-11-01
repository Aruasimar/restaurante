from sqlite3.dbapi2 import Date, Row
from flask import Flask, request, flash, session
from flask import render_template as render
from flask import redirect
from flask import request
from flask.helpers import url_for
import os
from flask.templating import render_template
from formulario import formRegistro, formLogin, formMod
import sqlite3, formulario
from sqlite3 import Error
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from markupsafe import escape
import sys

app = Flask(__name__)
app.secret_key = os.urandom(24)



# iNGRESO AL HOME
@app.route('/', methods=["GET"])
@app.route('/index', methods=["GET", "POST"])
def index():
    return render('index.html')

# Registro
@app.route('/registro', methods=["GET", "POST"])
def registrarse():
    form = formRegistro()
    return render("registro.html", form=form)

#Perfil del usuario, muestra los datos 
@app.route('/Perfil', methods=["GET", "POST"])
def perfil():
    correo = session.get('correo')
    try:
        with sqlite3.connect("E:/Isaura_proyectos/uninorte/ciclo3/ProyectoMinTicC3/restaurante.db") as con:
            con.row_factory = sqlite3.Row #Convierte la respuesta de la BD en un diccionario
            cur = con.cursor()
            cur.execute("SELECT * FROM Usuario WHERE email = ?", [correo])
            consulta = cur.fetchone()
            if consulta!=None:
                # print('-----------------------------------------------', file=sys.stderr)
                # print(consulta['id_usuario'], file=sys.stderr)
                # print(consulta['nombres'], file=sys.stderr)
                # print('-----------------------------------------------', file=sys.stderr)
                return render("perfil.html",consulta=consulta, username=session.get('username'))
            else:
                return 'no se encontró informacion'    
    except Error:
        con.rollback()
        print(Error)  
  

@app.route("/registro/save", methods=['POST'])
def registro_save():#tenia estudiante_save
    form = formRegistro()
    if request.method == 'POST':
        documento = escape(form.documento.data)
        nombres = escape(form.nombres.data)
        apellidos = escape(form.apellidos.data)
        tipo = escape(form.tipodocumento.data)
        fechanac = escape(form.fecha.data)
        #f1_str = fechanac.strftime('%d/%m/%Y')
        direccion = escape(form.direccion.data)
        celu = escape(form.celular.data)
        correo = escape(form.mail.data)
        usuario = escape(form.usuario.data)
        clave = escape(form.clave.data)
        hashed_pw = generate_password_hash(request.form["clave"], method="sha256")
        repetir = escape(form.repetir.data)
        politica = escape(form.politica.data)
        rol = 3
        try:
            with sqlite3.connect("E:/Isaura_proyectos/uninorte/ciclo3/ProyectoMinTicC3/restaurante.db") as con:
                cur = con.cursor() #Manipula la conexión a la BD
                cur.execute("INSERT INTO Usuario(id_usuario, nombres, apellidos, email, f_nac, t_doc, direccion, celular, politica) VALUES (?,?,?,?,?,?,?,?,?)", (documento, nombres, apellidos, correo, fechanac, tipo, direccion, celu, politica) )
                cur.execute("INSERT INTO Acceso(id_usuario, id_rol, username1, clave, username2) VALUES (?,?,?,?,?)", (documento, rol, usuario, hashed_pw, correo))
                con.commit() #Confirmar la transacción
                return redirect(url_for('ingresar'))
        
        except Error:
            print(Error)
    return "No se pudo guardar"


# Ingreso = Login
@app.route('/login', methods=["GET", "POST"])
def ingresar():
    form=formLogin()
    if request.method == "GET":
       return render("login.html", form=form)

    if request.method == "POST" and form.validate_on_submit():
        correo=escape(form.correo.data)
        clave=escape(form.clave1.data)
        try:
            with sqlite3.connect("E:/Isaura_proyectos/uninorte/ciclo3/ProyectoMinTicC3/restaurante.db") as con:
                cur = con.cursor()
                cur1 = con.cursor()
                consulta=cur.execute("select clave from Acceso where username2=?",[correo]).fetchone() #muestra el select clave en consulta, fetchone trae una lista
                consulta1=cur1.execute("select username1 from Acceso where username2=?",[correo]).fetchone() #muestra el select id_usuario en consulta, fetchone trae una lista
                if consulta!=None and consulta1!=None:
                    hashclave=consulta[0]
                    username=consulta1[0]
                    if check_password_hash(hashclave,clave):#compara que la clase sea igual a la que esta en la base de datos
                        session["username"]=username
                        session["correo"]=correo
                        return redirect(url_for('inicio'))
                    else:
                        return 'contraseña incorrecta'
                else:
                    return 'usuario no existe'
        except Error:
            print(Error)
    else:
        return render('login.html', form=form)

#vista si el cliente en su perfil quiere modificar la contraseña y cuando la vaya a recuperar
@app.route('/modificacion', methods=["GET"])
def modificacion():
    #return render('modificacion.html', username=session.get('username'))
    return 'pagina en construccion'

@app.route('/modificar', methods=["GET","POST"])
def modificar():
    form=formMod()
    username=session.get('username')
    correo=session.get('correo')
    if request.method=="GET":
        return render("modifcacion.html", form=form)
    
    if request.form=="POST" and form.validate_on_submit():
        nueva=escape(form.nueva.data)
        confirmar=escape(form.confirmacion.data)
        hashed_pw = generate_password_hash(request.form["nueva"], method="sha256")
        try:
            with sqlite3.connect("E:/Isaura_proyectos/uninorte/ciclo3/ProyectoMinTicC3/restaurante.db") as con:
                if nueva==confirmar:
                    cur = con.cursor()
                    cur.execute("UPDATE Acceso SET clave=? WHERE username1='"+username+"' AND username2='"+correo+"' ",[hashed_pw])
                    con.commit()
                    if con.total_changes >0:
                        mensaje="contraseña modificada"
                        return redirect(url_for('perfil'))
                        # print('-----------------------------------------------', file=sys.stderr)
                        # print(consulta['id_usuario'], file=sys.stderr)
                        # print(consulta['nombres'], file=sys.stderr)
                        # print('-----------------------------------------------', file=sys.stderr)
                    else:
                        mensaje="No se pudo modificar la contraseña"
                else:
                    return 'las contraseñas no coinciden'    
        except Error:
            con.rollback()
            print(Error)  
    else:
        return render('modificacion.html', form=form)




    

@app.route('/inicio', methods=["GET", "POST"])
def inicio():
    return render('inicio.html', username=session.get('username'))


# Salir
@app.route('/salir', methods=["GET","POST"])
def salir():
    #session.pop("username", None)
    session.clear()
    return redirect(url_for('index'))#quedé por aqui

# Acceso a Dashboard


@app.route('/dashboard/', methods=["GET", "POST"])
def dashboard():
    return render('dashboard/dashboard.html')

# Acceso a gestión de productos


@app.route('/productos', methods=["GET", "POST"])
def productos():
    return "Página de productos"


# Acceso a lista de deseos
@app.route('/deseos', methods=["GET", "POST"])
def deseos():
    return render('listadeseos.html')


# Acceso a gestión de pedidos
@app.route('/pedidos', methods=["GET", "POST"])
def pedidos():
    return render('listapedidos.html')


@app.route('/usuario')
def usuario():
    return render('usuarios.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
