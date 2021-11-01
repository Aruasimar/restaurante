from sqlite3.dbapi2 import Date, enable_callback_tracebacks
from typing import Match

from flask.globals import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, PasswordField, IntegerField
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import DataRequired, EqualTo, length, Email

class formRegistro(FlaskForm):
    nombres = StringField('Nombres', validators=[DataRequired(message='No dejar vacio'), length(min=3, max=25, message=('Ingrese nombres validos'))], render_kw={'class':'form-control' } )
    apellidos = StringField('Apellidos', validators=[DataRequired(message='No dejar vacio')], render_kw={'class':'form-control' } )
    tipodocumento = SelectField('Tipo de Documento', choices=[('Tipo de Documento'),('Cedula de Ciudadanía'),('Tarjeta de Extranjería'),('Numero de Pasaporte')], validators=[DataRequired(message='por favor seleccione el tipo de documento')], render_kw={'class':'form-select'} )
    documento = IntegerField('Número de Documento', validators=[DataRequired(message='No dejar vacio'), length(min=7, max=10, message=('numeros sin puntos entre 7 y 10 digitos'))], render_kw={'class':'form-control' } )
    fecha = DateField('Fecha de Nacimiento', validators=[DataRequired()], render_kw={'class':'form-control', 'id':'start' } )
    direccion = StringField('Dirección', validators=[DataRequired(message='No dejar vacio')], render_kw={'class':'form-control' } )
    celular = IntegerField('Número de Celular', validators=[DataRequired(message='No dejar vacio'), length(min=10, max=10, message=('ingrese un celular valido'))], render_kw={'class':'form-control' } )
    mail = EmailField('Email', validators=[DataRequired(message='No dejar vacio'), Email(message='Ingrese un mail valido')], render_kw={'class':'form-control' } )
    usuario = StringField('Nombre de Usuario', validators=[DataRequired(message='No dejar vacio'), length(min=4, max=8, message=('Ingrese un usuario entre 4 y 8 caracteres'))], render_kw={'class':'form-control' } )
    clave = PasswordField('Contraseña', validators=[DataRequired(message='No dejar vacio'), length(min=8, max=12, message=('contraseña entre 8 a 12 caracteres'))], render_kw={'class':'form-control' } )
    repetir = PasswordField('Confirmar Contraseña', validators=[DataRequired(message='No dejar vacio'), EqualTo('clave','Contraseñas inconsistentes')], render_kw={'class':'form-control' } )
    politica = BooleanField('Acepto la politica de tratamiento y uso datos personales.', validators=[DataRequired(message='Debe aceptar la politica de datos')], render_kw={'class':'form-check-input' } )

    enviar = SubmitField('Registrarse', render_kw={'onmouseover':'guardarUser()', 'class':'btn btn-primary mb-2'} )


class  formLogin(FlaskForm):
    correo = EmailField('Usuario', validators=[DataRequired(message='Por favor ingrese el correo con el que se registró'), Email(message='Ingrese un mail valido')], render_kw={'class':'form-control'} )
    clave1 = PasswordField('Clave', validators=[DataRequired(message='Por favor ingrese su contraseña'), length(min=8, max=12, message=('contraseña invalida: entre 8 a 12 caracteres'))], render_kw={'class':'form-control', 'placeholder':'Contraseña', 'id':'password'} )
    enviar1 = SubmitField('Iniciar Sesion', render_kw={'class':'btn btn-primary'} )
    
class formMod(FlaskForm):
    nueva = PasswordField('Nueva contraseña', validators=[DataRequired(message='Por favor ingrese su contraseña'), length(min=8, max=12, message=('contraseña invalida: entre 8 a 12 caracteres'))], render_kw={'class':'form-control', 'placeholder':'Contraseña', 'id':'password'} )
    confirmacion = PasswordField('Confirmar contraseña', validators=[DataRequired(message='Por favor ingrese su contraseña'), EqualTo('clave','Contraseñas inconsistentes'), length(min=8, max=12, message=('contraseña invalida: entre 8 a 12 caracteres'))], render_kw={'class':'form-control', 'placeholder':'Contraseña', 'id':'password'} )
    Modificar = SubmitField('Modificar', render_kw={'class':'btn btn-primary'} )