

$(document).ready(function () {
    
    //-------------VALIDAR NOMBRE------------------------//
    $("#inputNombre").keyup(function () {

        $.ajax({
            url: "/Validacion/ValidarNombre/",
            data:
            {
                nombre: $("#inputNombre").val()
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {


                    switch (result.resultado.toString()) {
                        case "1"://disponible
                            $("#inputNombre").css("background-color", "#ffffff");
                            $("#divAlertNombre").hide("slow");
                            break;
                        case "-1"://caracteres invalidos
                            $("#inputNombre").css("background-color", "#ffffff");
                            $("#divAlertNombre").show("slow");
                            document.getElementById('labelAlertNombre').textContent = "Caracteres invalidos";
                            break;
                        case "-2"://vacio
                            $("#inputNombre").css("background-color", "#ffffff");
                            $("#divAlertNombre").show("slow");
                            document.getElementById('labelAlertNombre').textContent = "Campo no puede quedar vacio";

                            break;
                        case "-3"://error metodo
                            $("#inputNombre").css("background-color", "#ffffff");
                            $("#divAlertNombre").hide("slow");
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

    //-------------VALIDAR APELLIDOS------------------------//
    $("#inputApellido").keyup(function () {

        $.ajax({
            url: "/Validacion/ValidarApellidos/",
            data:
            {
                apellidos: $("#inputApellido").val()
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {


                    switch (result.resultado.toString()) {
                        case "1"://disponible
                            $("#inputApellido").css("background-color", "#ffffff");
                            $("#divAlertApellido").hide("slow");
                            break;
                        case "-1"://caracteres invalidos
                            $("#inputApellido").css("background-color", "#ffffff");
                            $("#divAlertApellido").show("slow");
                            document.getElementById('labelAlertApellido').textContent = "Caracteres invalidos";
                            break;
                        case "-2"://vacio
                            $("#inputApellido").css("background-color", "#ffffff");
                            $("#divAlertApellido").show("slow");
                            document.getElementById('labelAlertApellido').textContent = "Campo no puede quedar vacio";

                            break;
                        case "-3"://error metodo
                            $("#inputApellido").css("background-color", "#ffffff");
                            $("#divAlertApellido").hide("slow");
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
    //-------------VALIDAR CORREO------------------------//
    $("#inputCorreo").keyup(function () {

        $.ajax({
            url: "/Validacion/ValidarCorreo/",
            data:
            {
                correo: $("#inputCorreo").val(),
                modificacion: true
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {


                    switch (result.resultado.toString()) {
                        case "1"://disponible
                            $("#inputCorreo").css("background-color", "#ffffff");
                            $("#divAlertCorreo").hide("slow");
                            break;
                        //case "-1"://caracteres invalidos
                        //    $("#inputCorreo").css("background-color", "#ff3c335c");
                        //    $("#divAlertCorreo").show("slow");
                        //    document.getElementById('labelAlertCorreo').textContent = "Caracteres invalidos";
                        //    break;
                        case "-2"://vacio
                            $("#inputCorreo").css("background-color", "#ffffff");
                            $("#divAlertCorreo").show("slow");
                            document.getElementById('labelAlertCorreo').textContent = "Campo no puede quedar vacio";

                            break;
                        case "-3"://error metodo
                            $("#inputCorreo").css("background-color", "#ffffff");
                            $("#divAlertCorreo").hide("slow");
                            break;
                        case "-4":
                            $("#inputCorreo").css("background-color", "#ff3c335c");
                            $("#divAlertCorreo").show("slow");
                            document.getElementById('labelAlertCorreo').textContent = "Correo ya registrado";
                            breaK;
                    }

                }
            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })
    });
    //-------------VALIDAR TELEFONO------------------------//
    $("#inputTelefono").keyup(function () {

        $.ajax({
            url: "/Validacion/ValidarTelefono/",
            data:
            {
                telefono: $("#inputTelefono").val(),
                modificacion:true
               
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {


                    switch (result.resultado.toString()) {
                        case "1"://disponible
                            $("#inputTelefono").css("background-color", "#ffffff");
                            $("#divAlertTelefono").hide("slow");
                            break;
                        case "-1"://caracteres invalidos
                            $("#inputTelefono").css("background-color", "#ffffff");
                            $("#divAlertTelefono").show("slow");
                            document.getElementById('labelAlertTelefono').textContent = "Caracteres invalidos";
                            break;
                        case "-2"://vacio
                            $("#inputTelefono").css("background-color", "#ffffff");
                            $("#divAlertTelefono").hide("slow");
                            break;
                        case "-3"://error metodo
                            $("#inputTelefono").css("background-color", "#ffffff");
                            $("#divAlertTelefono").hide("slow");
                            break;
                        case "-4":
                            $("#inputTelefono").css("background-color", "#ff3c335c");
                            $("#divAlertTelefono").show("slow");
                            document.getElementById('labelAlertTelefono').textContent = "Telefono ya registrado";
                            breaK;


                    }

                }
            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })
    });
    //BOTON CANCELAR DATOS PERSONALES//
    $("#btnCancelarDatosP").click(function () {
        
        $.ajax({
            url: "/Validacion/ObtenerDatosOriginalesUsuario/",
            data:
            {

            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    //alert(JSON.stringify(result));
                    document.getElementById('inputNombre').value = result.nombre.toString();
                    document.getElementById('inputApellido').value = result.apellido.toString();
                    document.getElementById('inputCorreo').value = result.correo.toString();
                    document.getElementById('inputTelefono').value = result.telefono.toString();
                   

                    $('#inputcodigoTelefono').empty();

                    result.codigos.forEach(function (item) {
                        //alert(result.direccion.pais);
                        LlenarCodigos(item, result.codigo);
                    });
                    $("#inputNombre").css("background-color", "#ffffff");
                    $("#divAlertNombre").hide("slow");
                    document.getElementById('labelAlertNombre').textContent = "";

                    $("#inputApellido").css("background-color", "#ffffff");
                    $("#divAlertApellido").hide("slow");
                    document.getElementById('labelAlertApellido').textContent = "";

                    $("#inputCorreo").css("background-color", "#ffffff");
                    $("#divAlertCorreo").hide("slow");
                    document.getElementById('labelAlertCorreo').textContent = "";

                    $("#inputTelefono").css("background-color", "#ffffff");
                    $("#divAlertTelefono").hide("slow");
                    document.getElementById('labelAlertTelefono').textContent = "";

                    $("#divAlertDatosPersonales").hide("slow");
                    document.getElementById('labelAlertDatosPersonales').textContent = "";
                }


            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })
    });

    //BOTON GUARDAR DATOS PERSONALES//
    $("#btnGuardarDatosP").click(function () {
        var codigo = document.getElementById("inputcodigoTelefono");
        $.ajax({
            url: "/Validacion/GuardarDatosPersonales/",
            data:
            {
                nombre: $("#inputNombre").val(),
                apellidos: $("#inputApellido").val(),
                correo: $("#inputCorreo").val(),
                codigoTelefono: codigo.options[codigo.selectedIndex].value,
                telefono: $("#inputTelefono").val(),
                modificacion: true
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    if (result.resultado == 1) {

                        $("#divAlertDatosPersonales").show("slow");
                        document.getElementById('labelAlertDatosPersonales').textContent = result.mensaje;
                        location.reload();
                    }
                    else {
                        $("#divAlertDatosPersonales").show("slow");
                        document.getElementById('labelAlertDatosPersonales').textContent = result.mensaje;
                    }
                }


            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })
    });
    function LlenarCodigos(item, codigoSeleccionado) {
        
        if (item["value"] == codigoSeleccionado)
            document.querySelector('#inputcodigoTelefono').add(new Option(item["text"], item["value"], true, true));
        else
            document.querySelector('#inputcodigoTelefono').add(new Option(item["text"], item["value"]));
    }

    //MODAL DATOS CUENTA
    //---------------------VALIDAR USUARIO-----------------------//
    $("#inputUsuario").keyup(function () {

        $.ajax({
            url: "/Validacion/ValidarUsuario/",
            data:
            {
                usuario: $("#inputUsuario").val(),
                modificacion:true
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    /* alert("done")*/




                    switch (result.resultado.toString()) {
                        case "1": //1 todo bien
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
                            document.getElementById('labelAlertUsuario').textContent = "No puede ser mayor a 20 caracteres";
                            break;
                        case "-6": //-6 no disponible
                            $("#inputUsuario").css("background-color", "#ff3c335c");
                            $("#divAlertUsuario").show("slow");
                            //document.getElementById('labelAlertNombre').innerHTML = "Usuario no disponible";
                            document.getElementById('labelAlertUsuario').textContent = "Usuario no disponible";
                            break;


                    }
                    //if (result.resultado == "1")
                    //{
                    //    /*alert("disponible")*/
                    //    $("#inputUsuario").css("background-color", "#8edd848f");
                    //    $("#divAlertUsuario").hide("slow");
                    //}
                    //else {
                    //    $("#inputUsuario").css("background-color", "#ff3c335c");
                    //    $("#divAlertUsuario").show("slow");
                    //   /* alert("ocupado")*/
                    //}
                }
            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })
    });
    //INPUT CONTRASEÑA ACTUAL//
    $("#inputContraseñaActual").keyup(function () {

        $.ajax({
            url: "/Validacion/ValidarContraseñaActual/",
            data:
            {
                contraseña: $("#inputContraseñaActual").val()
                
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    switch (result.resultado.toString()) {
                        case "1"://todo correcto
                            $("#inputContraseñaActual").css("background-color", "#ffffff");
                            $("#divAlertContraseñaActual").hide("slow");
                            break;
                        case "-1"://no coinciden
                            $("#inputContraseñaActual").css("background-color", "#ffffff");
                            $("#divAlertContraseñaActual").show("slow");
                            document.getElementById('labelAlertContraseñaActual').textContent = "Las contraseñas es incorrecta";
                            break;
                        case "-2"://vacio
                            $("#inputContraseñaActual").css("background-color", "#ffffff");
                            $("#divAlertContraseñaActual").show("slow");
                            document.getElementById('labelAlertContraseñaActual').textContent = "Campo no puede estar vacio";
                            break;
                        case "-3"://error metodo
                            $("#inputContraseñaActual").css("background-color", "#ffffff");
                            $("#divAlertContraseñaActual").hide("slow");
                            break;
                        case "-4"://-4longitud minima
                            $("#inputContraseñaActual").css("background-color", "#ffffff");
                            $("#divAlertContraseñaActual").show("slow");
                            document.getElementById('labelAlertContraseñaActual').textContent = "No puede ser menor a 8 caracteres";
                            break;
                        case "-5"://-5 longitud maxima
                            $("#inputContraseñaActual").css("background-color", "#ffffff");
                            $("#divAlertContraseñaActual").show("slow");
                            document.getElementById('labelAlertContraseñaActual').textContent = "No puede ser mayor a 25 caracteres";
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
    //---------------------VALIDAR CONTRASEÑA NUEVA-----------------------//
    $("#inputContraseña").keyup(function () {

        $.ajax({
            url: "/Validacion/ValidarContraseña/",
            data:
            {
                contraseña: $("#inputContraseña").val()
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
                            breaK;


                    }
                }
            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })
    });
    //-------------VALIDAR CONTRASEÑAS IGUALES------------------------//
    //INPUT CONTRASEÑA NUEVA//
    $("#inputContraseña").keyup(function () {

        $.ajax({
            url: "/Validacion/ValidarConfirmarContraseña/",
            data:
            {
                contraseña: $("#inputContraseña").val(),
                contraseñaconfirmar: $("#inputConfirmarContraseña").val()
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {


                    switch (result.resultado.toString()) {
                        case "1"://todo correcto
                            $("#inputConfirmarContraseña").css("background-color", "#ffffff");
                            $("#divAlertConfirmarContraseña").hide("slow");
                            break;
                        case "-1"://no coinciden
                            $("#inputConfirmarContraseña").css("background-color", "#ffffff");
                            $("#divAlertConfirmarContraseña").show("slow");
                            document.getElementById('labelAlertConfirmarContraseñae').textContent = "Las contraseñas no coinciden";
                            break;
                        //case "-2"://vacio
                        //    $("#inputConfirmarContraseña").css("background-color", "#ffffff");
                        //    $("#divAlertConfirmarContraseña").show("slow");
                        //    document.getElementById('labelAlertConfirmarContraseñae').textContent = "Campo no puede quedar vacio";

                        //    break;
                        case "-3"://error metodo
                            $("#inputConfirmarContraseña").css("background-color", "#ffffff");
                            $("#divAlertConfirmarContraseña").hide("slow");
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
    //INPUT CONFIRMAR CONTRASEÑA//
    $("#inputConfirmarContraseña").keyup(function () {

        $.ajax({
            url: "/Validacion/ValidarConfirmarContraseña/",
            data:
            {
                contraseña: $("#inputContraseña").val(),
                contraseñaconfirmar: $("#inputConfirmarContraseña").val()
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {


                    switch (result.resultado.toString()) {
                        case "1"://todo correcto
                            $("#inputConfirmarContraseña").css("background-color", "#ffffff");
                            $("#divAlertConfirmarContraseña").hide("slow");
                            break;
                        case "-1"://no coinciden
                            $("#inputConfirmarContraseña").css("background-color", "#ffffff");
                            $("#divAlertConfirmarContraseña").show("slow");
                            document.getElementById('labelAlertConfirmarContraseñae').textContent = "Las contraseñas no coinciden";
                            break;
                        case "-2"://vacio
                            $("#inputConfirmarContraseña").css("background-color", "#ffffff");
                            $("#divAlertConfirmarContraseña").show("slow");
                            document.getElementById('labelAlertConfirmarContraseñae').textContent = "Campo no puede quedar vacio";

                            break;
                        case "-3"://error metodo
                            $("#inputConfirmarContraseña").css("background-color", "#ffffff");
                            $("#divAlertConfirmarContraseña").hide("slow");
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
    //-----------------------------------------------------------------//
    //BOTON CANCELAR DATOS CUENTA CONTRASEÑA//
    $("#btnCancelarDatosCC").click(function () {

        $.ajax({
            url: "/Validacion/ObtenerDatosOriginalesUsuario/",
            data:
            {

            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                   
                    document.getElementById('inputContraseñaActual').value = "";
                    document.getElementById('inputContraseña').value = "";
                    document.getElementById('inputConfirmarContraseña').value = "";

                    $("#inputContraseñaActual").css("background-color", "#ffffff");
                    $("#divAlertContraseñaActual").hide("slow");
                    document.getElementById('labelAlertContraseñaActual').textContent = "";

                    $("#inputContraseña").css("background-color", "#ffffff");
                    $("#divAlertContraseña").hide("slow");
                    document.getElementById('labelAlertContraseña').textContent = "";

                    $("#inputConfirmarContraseña").css("background-color", "#ffffff");
                    $("#divAlertConfirmarContraseña").hide("slow");
                    document.getElementById('labelAlertConfirmarContraseñae').textContent = "";

                    $("#divAlertDatosCuentaC").hide("slow");
                    document.getElementById('labelAlertDatosCuentaC').textContent = "";

                }


            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })
    });
    
    //BOTON GUARDAR DATOS CUENTA CONTRASEÑA//
    $("#btnGuardarDatosCC").click(function () {
        
        $.ajax({
            url: "/Validacion/GuardarDatosCuentaC/",
            data:
            {
                contraseñaActual: $("#inputContraseñaActual").val(),
                contraseñaNueva: $("#inputContraseña").val().toString(),
                contraseñaNuevaConfirmar: $("#inputConfirmarContraseña").val().toString()
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    if (result.resultado == 1) {

                        $("#divAlertDatosCuentaC").show("slow");
                        document.getElementById('labelAlertDatosCuentaC').textContent = result.mensaje;
                        location.reload();
                    }
                    else {
                        $("#divAlertDatosCuentaC").show("slow");
                        document.getElementById('labelAlertDatosCuentaC').textContent = result.mensaje;
                    }
                }


            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })
    });

    //BOTON CANCELAR DATOS CUENTA USUARIO//
    $("#btnCancelarDatosCU").click(function () {

        $.ajax({
            url: "/Validacion/ObtenerDatosOriginalesUsuario/",
            data:
            {

            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    document.getElementById('inputUsuario').value = result.usuario.toString();
                    document.getElementById('inputContraseñaActual').value = "";
                   

                    $("#inputUsuario").css("background-color", "#ffffff");
                    $("#divAlertUsuario").hide("slow");
                    document.getElementById('labelAlertUsuario').textContent = "";

                    $("#divAlertDatosCuenta").hide("slow");
                    document.getElementById('labelAlertDatosCuenta').textContent = "";

                    $("#inputContraseñaActual").css("background-color", "#ffffff");
                    $("#divAlertContraseñaActual").hide("slow");
                    document.getElementById('labelAlertContraseñaActual').textContent = "";

                }


            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })
    });

    //BOTON GUARDAR DATOS CUENTA USUARIO//
    $("#btnGuardarDatosCU").click(function () {

        $.ajax({
            url: "/Validacion/GuardarDatosCuentaU/",
            data:
            {
                usuario: $("#inputUsuario").val()
               
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    if (result.resultado == 1) {

                        $("#divAlertDatosCuenta").show("slow");
                        document.getElementById('labelAlertDatosCuenta').textContent = result.mensaje;
                        location.reload();
                    }
                    else {
                        $("#divAlertDatosCuenta").show("slow");
                        document.getElementById('labelAlertDatosCuenta').textContent = result.mensaje;
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

