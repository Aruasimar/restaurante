function guardarUser(){
    document.getElementById("formulario").action="/registro/save"//**estaba "/registro/save"
}

function desloguear(){
    document.getElementById("salir").action="/salir"
}

function consultarUser(){
    document.getElementById("formulario").action="/usuario/get"
}
function listarUser(){
    document.getElementById("formulario").action="/usuario/list"
}
function actualizarUser(){
    document.getElementById("formulario").action="/usuario/update"
}
function eliminarUser(){
    document.getElementById("formulario").action="/usuario/delete"
}

function muestra(obj){
    var obj = document.getElementById("repetir");
    obj.type = "text";    
}

function ocultar(obj){
    var obj = document.getElementById("repetir");
    obj.type = "password";
}

function mostrarPassword(obj) {
    var obj = document.getElementById("clave");
    obj.type = "text";
}

function ocultarPassword(obj) {
    var obj = document.getElementById("clave");
    obj.type = "password";
}

