
    $(document).ready(function(){
        $("#inputUsuario").keydown(function () {
           /* $("#inputUsuario").css("background-color", "yellow");*/
        });

         //-------------VALIDAR NOMBRE------------------------//
        $("#inputNombre").keyup(function(){
           
            $.ajax({
                url: "/ValidarNombre/",
                data:
                {
                    nombre: $("#inputNombre").val().toString()
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
                url: "/ValidarApellidos/",
                data:
                {
                    apellidos: $("#inputApellido").val().toString()
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
                url: "/ValidarCorreo/",
                data:
                {
                    correo: $("#inputCorreo").val().toString()
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
        //-------------VALIDAR TELEFONO------------------------//
        $("#inputTelefono").keyup(function () {

            $.ajax({
                url: "/ValidarTelefono/",
                data:
                {
                    telefono: $("#inputTelefono").val().toString()
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
        //---------------------VALIDAR USUARIO-----------------------//
        $("#inputUsuario").keyup(function () {

            $.ajax({
                url: "/ValidarUsuario/",
                data:
                {
                    usuario: $("#inputUsuario").val().toString()
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
                                document.getElementById('labelAlertUsuario').textContent = "No puede ser mayor a 25 caracteres";
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
        //---------------------VALIDAR CONTRASEÑA-----------------------//
        $("#inputContraseña").keyup(function () {

            $.ajax({
                url: "/ValidarContraseña/",
                data:
                {
                    contraseña: $("#inputContraseña").val().toString()
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
        //INPUT CONTRASEÑA//
        $("#inputContraseña").keyup(function () {

            $.ajax({
                url: "/ValidarConfirmarContraseña/",
                data:
                {
                    contraseña: $("#inputContraseña").val().toString(),
                    contraseñaconfirmar: $("#inputConfirmarContraseña").val().toString()
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
                url: "/ValidarConfirmarContraseña/",
                data:
                {
                    contraseña: $("#inputContraseña").val().toString(),
                    contraseñaconfirmar: $("#inputConfirmarContraseña").val().toString()
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
        //----------------------------------------------------------------------------------//

        //BOTON CREAR CUENTA//
        $("#btnCrearCuenta").click(function () {

            var codigo = document.getElementById("inputcodigoTelefono");
            $.ajax({
                url: "/CrearCuenta/",
                data:
                {
                    //string nombre,string apellido,string correo,string telefono,string usuario,string contraseña,string contraseñaConf
                    nombre: $("#inputNombre").val().toString(),
                    apellido: $("#inputApellido").val().toString(),
                    correo: $("#inputCorreo").val().toString(),
                    telefono: $("#inputTelefono").val().toString(),
                    usuario: $("#inputUsuario").val().toString(),
                    contraseña: $("#inputContraseña").val().toString(),
                    contraseñaConf: $("#inputConfirmarContraseña").val().toString(),
                    codigoTelefono: codigo.options[codigo.selectedIndex].value
                },
                type: "POST"
            })
                .done(function (result) {
                    if (result != null) {

                        //alert("" + result.resultadoM.toString() + "" + result.resultadoC.toString())
                        switch (result.resultadoC.toString()) {
                            case "1"://todo correcto
                              
                                $("#divAlertCrearCuenta").show("slow");
                                document.getElementById('labelAlertCrearCuenta').textContent = result.resultadoM.toString();
                                var fecha = new Date(result.fechaExpiracion.toString());
                                //var fecha = new Date(2023,1,02,11,20);
                                document.cookie = "SesionUsuario=" + result.token.toString() + "; expires=" + fecha.toUTCString() + ";path=/";
                                var form = document.getElementById("formularioRegistro");
                                form.submit();
                                window.location.href = '/';
                                
                                break;
                            default://datos erroneos
                               
                                $("#divAlertCrearCuenta").show("slow");
                                document.getElementById('labelAlertCrearCuenta').textContent = result.resultadoM.toString();
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

