////var colapsado = true;
var idComentario = -1;
var idUsuario = -1;

function EliminarComentario(idCom)
{
    
    $.ajax({
        url: "/Validacion/EliminarComentario/",
        data:
        {
            idcomentario: idCom
        },
        type: "POST"
    })
        .done(function (result) {
            if (result != null) {
                //alert(JSON.stringify(result));

                switch (result.resultado) {
                    case 1:
                        location.reload();
                        break;
                    case -1:
                        break;
                   
                }
            }
        })
        .fail(function (result) {
            if (result != null) {
                /*alert("fail")*/
            }
        })
}
function Colapse(pos)
{
    //colapsado = !colapsado;

    if (document.getElementById("btnColapse " + pos).classList.contains('fa-square-caret-up')) {
        document.getElementById("btnColapse "+pos).classList.remove('fa-square-caret-up');
        document.getElementById("btnColapse " + pos).classList.add('fa-square-caret-down');
    }
    else {
        document.getElementById("btnColapse " + pos).classList.remove('fa-square-caret-down');
        document.getElementById("btnColapse " + pos).classList.add('fa-square-caret-up');
    }

}
function EditarComentario(idCom,idU)
{
    setComentario(idCom,idU);
    if (getComentario() != -1) {
        $.ajax({
            url: "/Validacion/ObtenerInformacionComentario/",
            data:
            {
                idcomentario: getComentario()
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    //alert(JSON.stringify(result));

                    switch (result.resultado) {
                        case 1:
                            if (result.comentario != null) {
                                document.getElementById('inputTema').value = result.comentario[0].tema;
                                document.getElementById('inputComentario').value = result.comentario[0].comentario;
                            }
                            break;
                        case -1:
                            break;

                    }
                }
            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })
    }
  
}
function setComentario(idCom,idUsu) {
    this.idComentario = idCom;
    this.idUsuario = idUsu;
    //alert(this.idComentario);
    if (this.idComentario != -1) {
        //alert("modifico");
        document.getElementById('staticBackdropLabelComentario').textContent  = 'Modificar comentario';
    }
    else {
        //alert("agrego");
        document.getElementById('staticBackdropLabelComentario').textContent  = "Agregar comentario";
    }
}
function getComentario() {
    return this.idComentario;
}
function getUsuario() {
    return this.idUsuario;
}

$(document).ready(function () {
    $("#btnCancelarDatosCOM").click(function () {

        //setComentario(-1);
        document.getElementById('inputTema').value = "";
        document.getElementById('inputComentario').value = "";
        $("#divAlertComentario").hide("slow");
        document.getElementById('labelAlertComentario').textContent = "";
        $("#divAlertTema").hide("slow");
        document.getElementById('labelAlertTema').textContent = "";
        

       
    });

    $("#btnGuardarComentario").click(function () {

        if (getComentario() != -1)//modifica
        {
            $.ajax({
                url: "/Validacion/ModificarComentarioUsuario/",
                data:
                {
                    idcomentario: getComentario(),
                    tema: $("#inputTema").val().toString(),
                    comentario: $("#inputComentario").val().toString(),

                },
                type: "POST"
            })
                .done(function (result) {
                    if (result != null) {
                        //alert(JSON.stringify(result));

                        switch (result.resultado) {
                            case 1://1 todo bien
                                location.reload();
                                break;
                            case -1://-1 error agregar
                                $("#inputComentario").css("background-color", "#ffffff");
                                $("#divAlertComentario").show("slow");
                                document.getElementById('labelAlertComentario').textContent = "Error al agregar,intente de nuevo o mas tarde";
                                break;
                            case -2://-2 tema vacio
                                $("#inputTema").css("background-color", "#ffffff");
                                $("#divAlertTema").show("slow");
                                document.getElementById('labelAlertTema').textContent = "Campo no puede quedar vacio";
                                break;
                            case -4://-4 tema longitud minima
                                $("#inputTema").css("background-color", "#ffffff");
                                $("#divAlertTema").show("slow");
                                document.getElementById('labelAlertTema').textContent = "No puede ser menor a 8 caracteres";
                                break;
                            case -5://-5 tema longitud maxima
                                $("#inputTema").css("background-color", "#ffffff");
                                $("#divAlertTema").show("slow");
                                document.getElementById('labelAlertTema').textContent = "No puede ser mayor a 50 caracteres";
                                break;
                            case -6://-6 comentario vacio
                                $("#inputComentario").css("background-color", "#ffffff");
                                $("#divAlertComentario").show("slow");
                                document.getElementById('labelAlertComentario').textContent = "Campo no puede quedar vacio";
                                break;
                        }
                    }
                })
                .fail(function (result) {
                    if (result != null) {
                        /*alert("fail")*/
                    }
                })
        }
        else//agrega
        {
            $.ajax({
                url: "/Validacion/AgregarComentario/",
                data:
                {
                    idUsuario: getUsuario(),
                    tema: $("#inputTema").val().toString(),
                    comentario: $("#inputComentario").val().toString(),
                   
                },
                type: "POST"
            })
                .done(function (result) {
                    if (result != null) {
                        //alert(JSON.stringify(result));
                        switch (result.resultado)
                        {
                            case 1://1 todo bien
                                location.reload();
                                break;
                            case -1://-1 error agregar
                                $("#inputComentario").css("background-color", "#ffffff");
                                $("#divAlertComentario").show("slow");
                                document.getElementById('labelAlertComentario').textContent = "Error al agregar,intente de nuevo o mas tarde";
                                break;
                            case -2://-2 tema vacio
                                $("#inputTema").css("background-color", "#ffffff");
                                $("#divAlertTema").show("slow");
                                document.getElementById('labelAlertTema').textContent = "Campo no puede quedar vacio";
                                break;
                            case -4://-4 tema longitud minima
                                $("#inputTema").css("background-color", "#ffffff");
                                $("#divAlertTema").show("slow");
                                document.getElementById('labelAlertTema').textContent = "No puede ser menor a 8 caracteres";
                                break;
                            case -5://-5 tema longitud maxima
                                $("#inputTema").css("background-color", "#ffffff");
                                $("#divAlertTema").show("slow");
                                document.getElementById('labelAlertTema').textContent = "No puede ser mayor a 50 caracteres";
                                break;
                            case -6://-6 comentario vacio
                                $("#inputComentario").css("background-color", "#ffffff");
                                $("#divAlertComentario").show("slow");
                                document.getElementById('labelAlertComentario').textContent = "Campo no puede quedar vacio";
                                break;
                        }
                    }
                })
                .fail(function (result) {
                    if (result != null) {
                        /*alert("fail")*/
                    }
                })
        }
    });

    //---------------------VALIDAR TEMA-----------------------//
    $("#inputTema").keyup(function () {

        $.ajax({
            url: "/Validacion/ValidarTema/",
            data:
            {
                tema: $("#inputTema").val().toString()
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                     //1 todo bien
                    //-2 vacio
                    //-3 error metodo
                    //-4longitud minima
                    //-5 longitud maxima
                    switch (result.resultado.toString()) {
                        case "1": //1 todo bien
                            $("#inputTema").css("background-color", "#ffffff");
                            $("#divAlertTema").hide("slow");
                            break;
                        case "-2": //-2 vacio
                            $("#inputTema").css("background-color", "#ffffff");
                            $("#divAlertTema").show("slow");
                            document.getElementById('labelAlertTema').textContent = "Campo no puede quedar vacio";

                            break;
                        case "-3": //-3 error metodo
                            $("#inputTema").css("background-color", "#ffffff");
                            $("#divAlertTema").hide("slow");
                            break;
                        case "-4"://longitud minima
                            $("#inputTema").css("background-color", "#ffffff");
                            $("#divAlertTema").show("slow");
                            document.getElementById('labelAlertTema').textContent = "No puede ser menor a 8 caracteres";
                            break;
                        case "-5"://longitud maxima
                            $("#inputTema").css("background-color", "#ffffff");
                            $("#divAlertTema").show("slow");
                            document.getElementById('labelAlertTema').textContent = "No puede ser mayor a 50 caracteres";
                            break;
                       
                        default:
                            $("#inputTema").css("background-color", "#ffffff");
                            $("#divAlertTema").hide("slow");
                            document.getElementById('labelAlertTema').textContent = "Error desconocido";
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

    $("#inputComentario").keyup(function () {

        $.ajax({
            url: "/Validacion/ValidarComentario/",
            data:
            {
                comentario: $("#inputComentario").val().toString()
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    //1 todo bien
                    //-2 vacio
                    //-3 error metodo
                    //-4longitud minima
                    //-5 longitud maxima
                    switch (result.resultado.toString()) {
                        case "1": //1 todo bien
                            $("#inputComentario").css("background-color", "#ffffff");
                            $("#divAlertComentario").hide("slow");
                            break;
                        case "-2": //-2 vacio
                            $("#inputComentario").css("background-color", "#ffffff");
                            $("#divAlertComentario").show("slow");
                            document.getElementById('labelAlertComentario').textContent = "Campo no puede quedar vacio";

                            break;
                        case "-3": //-3 error metodo
                            $("#inputComentario").css("background-color", "#ffffff");
                            $("#divAlertComentario").hide("slow");
                            break;
                       
                        default:
                            $("#inputComentario").css("background-color", "#ffffff");
                            $("#divAlertComentario").hide("slow");
                            document.getElementById('labelAlertComentario').textContent = "Error desconocido";
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