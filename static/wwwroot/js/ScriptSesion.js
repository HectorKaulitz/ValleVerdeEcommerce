$(document).ready(function () {
  

    
    //---------------------VALIDAR USUARIO-----------------------//
    $("#inputUsuario").keyup(function () {

        $.ajax({
            url: "/validarUsuarioInicioSesion/",
            data:
            {
                'usuario': $("#inputUsuario").val().toString()
            },
            type: "POST"
        })
            .done(function (result) {

                if (result != null) {
                    /* alert("done")*/
            //1 existe usuario
            //-1caracteres ivalidos
            //-2 vacio
            //-3 error metodo
            //-4longitud minima
            //-5 longitud maxima
            //-6 no existe
                    switch (result.resultado.toString()) {
                        case "1": //1 todo bien,si existe usuario
                            $("#inputUsuario").css("background-color", "#ffffff");
                            $("#divAlertUsuario").hide("slow");
                            break;

                        case "-1": //-1caracteres ivalidos
                            $("#inputUsuario").css("background-color", "#ffffff");
                            $("#divAlertUsuario").show("slow");
                            document.getElementById('labelAlertUsuario').textContent = "Caracteres invalidos";
                            break;
                        case "-2": //-2 vacio
                            $("#inputUsuario").css("background-color", "#ffffff");
                            $("#divAlertUsuario").show("slow");
                            document.getElementById('labelAlertUsuario').textContent = "Campo no puede quedar vacio";

                            break;
                        case "-3": //-3 error metodo
                            $("#inputUsuario").css("background-color", "#ffffff");
                            $("#divAlertUsuario").hide("slow");
                            break;
                        case "-4"://longitud minima
                            $("#inputUsuario").css("background-color", "#ffffff");
                            $("#divAlertUsuario").show("slow");
                            document.getElementById('labelAlertUsuario').textContent = "No puede ser menor a 8 caracteres";
                            break;
                        case "-5"://longitud maxima
                            $("#inputUsuario").css("background-color", "#ffffff");
                            $("#divAlertUsuario").show("slow");
                            document.getElementById('labelAlertUsuario').textContent = "No puede ser mayor a 25 caracteres";
                            break;
                        //case "-6": //-6 no existe usuario
                        //    $("#inputUsuario").css("background-color", "#ff3c335c");
                        //    $("#divAlertUsuario").show("slow");
                        //    document.getElementById('labelAlertUsuario').textContent = "Usuario no registrado";
                        //    break;
                        default://longitud maxima
                            $("#inputUsuario").css("background-color", "#ffffff");
                            $("#divAlertUsuario").hide("slow");
                            document.getElementById('labelAlertUsuario').textContent = "";
                            break;


                    }
                }
            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })
    });
    //---------------------VALIDAR CONTRASEÑA-----------------------//
    $("#inputContraseña").keyup(function () {

        $.ajax({
            url: "/validarContrasenaInicioSesion/",
            data:
            {
                'contrasena': $("#inputContraseña").val().toString()
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    /* alert("done")*/

                    switch (result.resultado.toString()) {
                        case "1"://correcto
                            $("#inputContraseña").css("background-color", "#ffffff");
                            $("#divAlertContraseña").hide("slow");
                            break;
                        case "-1"://caracteres invalidos
                            $("#inputContraseña").css("background-color", "#ff3c335c");
                            $("#divAlertContraseña").show("slow");
                            document.getElementById('labelAlertContraseña').textContent = "Caracteres invalidos";
                            break;
                        case "-2"://vacio
                            $("#inputContraseña").css("background-color", "#ffffff");
                            $("#divAlertContraseña").show("slow");
                            document.getElementById('labelAlertContraseña').textContent = "Campo no puede quedar vacio";
                            break;
                        case "-3"://error metodo
                            $("#inputContraseña").css("background-color", "#ffffff");
                            $("#divAlertContraseña").hide("slow");
                            break;
                        case "-4"://longitud minima
                            $("#inputContraseña").css("background-color", "#ffffff");
                            $("#divAlertContraseña").show("slow");
                            document.getElementById('labelAlertContraseña').textContent = "No puede ser menor a 8 caracteres";
                            break;
                        case "-5"://longitud maxima
                            $("#inputContraseña").css("background-color", "#ffffff");
                            $("#divAlertContraseña").show("slow");
                            document.getElementById('labelAlertContraseña').textContent = "No puede ser mayor a 25 caracteres";
                            breaK;
                        case "-6"://no contiene letras
                            $("#inputContraseña").css("background-color", "#ff3c335c");
                            $("#divAlertContraseña").show("slow");
                            document.getElementById('labelAlertContraseña').textContent = "Debe contener letra(s)";
                            break;
                        case "-7"://no contiene numeros
                            $("#inputContraseña").css("background-color", "#ff3c335c");
                            $("#divAlertContraseña").show("slow");
                            document.getElementById('labelAlertContraseña').textContent = "Debe contener numero(s)";
                            break;


                    }
                }
            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })
    });
    //BOTON INICIAR SESION//
    $("#btnIniciarSesion").click(function () {

        $.ajax({
            url: "/validarDatosInicioSesion",
            data:
            {
              
                'usuario': $("#inputUsuario").val().toString(),
                'contrasena': $("#inputContraseña").val().toString()
            },
            type: "POST"
        })
            .done(function (result) {
            //alert('hol'+JSON.stringify(result))
                if (result != null) {
             //1 coincide y esta activo
            //2 debe pasar la validacion de campos
            //-1 usuario no existe
            //-2 usuario existe,contraseña mal
            //-3 erro metodo/proced
            //-4 cuenta inactiva
                   
                    switch (result.resultado.toString()) {
                        case "1"://todo correcto
                            $("#divAlertIniciarSesion").show("slow");
                            document.getElementById('labelAlertIniciarSesion').textContent = "Validacion exitosa -" + result.token.toString();
                           
                            var fecha = new Date(result.fechaExpiracion.toString());
                            //var fecha = new Date(2023,1,02,11,20);
                            document.cookie = "SesionUsuario=" + result.token.toString() + "; expires=" + fecha.toUTCString()+";path=/";
                            var form =document.getElementById("formularioSesion");
                            //form.submit();
                            //document.cookie = "SesionUsuario=" + result.token.toString();
                           document.location.href="/";
                            break;
                        case "2"://debe pasar la validacion de campos

                            $("#divAlertIniciarSesion").show("slow");
                            document.getElementById('labelAlertIniciarSesion').textContent ="Datos en campos invalidos";
                            break;
                        case "-1"://usuario no existe

                            $("#divAlertIniciarSesion").show("slow");
                            document.getElementById('labelAlertIniciarSesion').textContent = "Usuario no existe";
                            break;
                        case "-2"://contraseña mal

                            $("#divAlertIniciarSesion").show("slow");
                            document.getElementById('labelAlertIniciarSesion').textContent = "Contraseña incorrecta";
                            break;
                        case "-2":// metodo/proc error

                            $("#divAlertIniciarSesion").show("slow");
                            document.getElementById('labelAlertIniciarSesion').textContent = "Error metodo";
                            break;
                        case "-4"://usuario inactivo/dado baja

                            $("#divAlertIniciarSesion").show("slow");
                            document.getElementById('labelAlertIniciarSesion').textContent = "Usuario inactivo";
                            break;
                        default:

                            $("#divAlertIniciarSesion").show("slow");
                            document.getElementById('labelAlertIniciarSesion').textContent = "Error desconocido";
                            break;

                    }

                }
            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })
    });

   
});