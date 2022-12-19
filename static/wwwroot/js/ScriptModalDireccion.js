var idDireccion = -1;
var idUsuario = -1;

function Editar(idDir) {
    //$("#inputPais").css("background-color", "yellow");
    setDireccion(idDir);
    //alert(this.idDireccion);
    $.ajax({
        async: false,
        url: "/ObtenerDatosDireccionUsuario/",
        data:
        {
            usuario: "-1",
            idDir: getDireccion()
        },
        type: "POST"
    })
        .done(function (result) {
            //direccion
            setUsuario(result.direccion.idUsuarioRegistrado);
            //alert(JSON.stringify(result));

            document.getElementById('inputCalle').value = result.direccion.calle;
            document.getElementById('inputNumeroExterior').value = result.direccion.numeroExterior;
            document.getElementById('inputNumeroInterior').value = result.direccion.numeroInterior;
            document.getElementById('inputDestinatario').value = result.direccion.destinatario;
            //alert(getUsuario() + " - " + getDireccion());
            //PAISES


            /* Remove all options from the select list */
            $('#inputPais').empty();

            result.paises.forEach(function (item) {
                //alert(result.direccion.pais);
                LlenarPaises(item, result.direccion.pais);
            });



                /* Remove all options from the select list */
                $('#inputEstado').empty();

                result.estados.forEach(function (item) {
                    //alert(result.direccion.pais);
                    LlenarEstados(item, result.direccion.estado);
                });


                $('#inputCiudad').empty();

                result.ciudades.forEach(function (item) {
                    //alert(result.direccion.pais);
                    LlenarCiudades(item, result.direccion.ciudad);
                });


                document.getElementById('inputCodigoPostal').value = result.direccion.codigoPostal;

            if (result.drop == 1) {
                document.getElementById("div-contenido-input-item-colonia").innerHTML = ` <select id="inputColonia" name="inputColonia" class="form form-control input-txt-item form-select" asp-items="" required style="text-align: center;"> </select>`;

                /* Remove all options from the select list */
                $('#inputColonia').empty();
                result.colonias.forEach(function (item) {
                    LlenarColonias(item, result.direccion.colonia);
                });
            }
            else {
              
            //muestra el input manual
            document.getElementById("div-contenido-input-item-colonia").innerHTML = ` <input value="" name="inputColonia" id="inputColonia" type="text" class="input-txt-item" placeholder="Campo obligatorio" required /> `;
            document.getElementById('inputColonia').value = result.direccion.colonia;
                
            }


            }).fail(function (result) {

                })
    }


function AsignarId(idDireccion) {
    setDireccion(idDireccion);
    setUsuario(-1);
    //alert(this.idDireccion);
}

function getDireccion() {
    return this.idDireccion;
}

function getUsuario() {
    return this.idUsuario;
}

function setUsuario(id) {
    this.idUsuario = id;
}

function setDireccion(idD) {
    this.idDireccion = idD;
}

$(document).ready(function () {
    $("#inputPais").change(function () {
        //$("#inputPais").css("background-color", "yellow");
        var sel = document.getElementById("inputPais");
        
        var text = sel.options[sel.selectedIndex].text;
        $.ajax({
            url: "/ObtenerEstadosPais/",
            data:
            {
                pais: text,
                iso3: $("#inputPais").val()
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    //alert(JSON.stringify(result));
                   
                    /* Remove all options from the select list */
                    $('#inputEstado').empty();
                    result.estados.forEach(function (item) {
                        LlenarEstados(item, "null")
                    });
                   
                    var selE = document.getElementById("inputEstado");
                    var textE = selE.options[selE.selectedIndex].text;


                    $.ajax({
                        url: "/ObtenerCiudadesEstadoPais/",
                        data:
                        {
                            pais: text,
                            estado: textE
                        },
                        type: "POST"
                    })
                        .done(function (resultC) {
                            if (resultC != null) {
                                //alert(JSON.stringify(result));

                                /* Remove all options from the select list */
                                $('#inputCiudad').empty();

                                resultC.ciudades.forEach(function (item) {
                                    LlenarCiudades(item, "null")
                                });
                            }


                        })
                        .fail(function (resultC) {
                            if (resultC != null) {
                                /*alert("fail")*/
                            }
                        })
                }


            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })

        

    });

    $("#inputEstado").change(function () {
        //$("#inputPais").css("background-color", "yellow");
        var sel = document.getElementById("inputPais");
        var selE = document.getElementById("inputEstado");

        var text = sel.options[sel.selectedIndex].text;
        var textE = selE.options[selE.selectedIndex].text;
        $.ajax({
            url: "/ObtenerCiudadesEstadoPais/",
            data:
            {
                pais: text,
                estado: textE
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    //alert(JSON.stringify(result));

                    /* Remove all options from the select list */
                    $('#inputCiudad').empty();

                    result.ciudades.forEach(function (item) {
                        LlenarCiudades(item, "null")
                    });
                }


            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })
    });

    $("#btnCancelarDatosAD").click(function () {
        //$("#inputPais").css("background-color", "yellow");
        setDireccion(-1);
        var sel = document.getElementById("inputPais");

        var text = sel.options[sel.selectedIndex].text;
        $.ajax({
            async: false,
            url: "/ObtenerEstadosPaisCiudadDefecto/",
            data:
            {
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    //alert(JSON.stringify(result));

                    /* Remove all options from the select list */
                    $('#inputEstado').empty();
                    $('#inputPais').empty();
                    $('#inputCiudad').empty();
                    document.getElementById('inputCodigoPostal').value = result.codigod;
                    document.getElementById('inputCalle').value = result.calle;
                    document.getElementById('inputNumeroExterior').value = result.exterior;
                    document.getElementById('inputNumeroInterior').value = result.interior;
                    document.getElementById('inputDestinatario').value = result.destinatario;
                    $("#divAlertDatosDireccion").hide("slow");
                    document.getElementById('labelAlertDatosDireccion').textContent ="";

                    result.paises.forEach(function(item)
                    {
                        LlenarPaises(item, result.pais);
                    });
                    

                    result.estados.forEach(function (item) {
                        LlenarEstados(item, result.estado);
                    });
                   

                    result.ciudades.forEach(function (item) {
                        LlenarCiudades(item, result.ciudad);
                    });

                    ObtenerColonias("");
                   

                }


            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })
    });

    $("#btnGuardarDatosAD").click(function ()
    {
        var pais = document.getElementById("inputPais");
        var estado = document.getElementById("inputEstado");
        //alert(getDireccion());
       
        $.ajax({
            url: "/GuardarDireccion/",
            data:
            {
                idDir: getDireccion(),
                ciudad: $("#inputCiudad").val(),
                colonia: $("#inputColonia").val(),
                calle: $("#inputCalle").val(),
                nexterior: $("#inputNumeroExterior").val(),
                ninterior: $("#inputNumeroInterior").val(),
                destinatario: $("#inputDestinatario").val(),
                isoPais: pais.options[pais.selectedIndex].value,
                pais: pais.options[pais.selectedIndex].text,
                estado: estado.options[estado.selectedIndex].text,
                codigoEstado: estado.options[estado.selectedIndex].value,
                codigoPostal: $("#inputCodigoPostal").val()
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                     //alert(JSON.stringify(result));

                    if (result.resultado == 1) {
                        
                        $("#divAlertDatosDireccion").show("slow");
                        document.getElementById('labelAlertDatosDireccion').textContent = result.mensaje;
                        location.reload();
                    }
                    else {
                        $("#divAlertDatosDireccion").show("slow");
                        document.getElementById('labelAlertDatosDireccion').textContent = result.mensaje;
                    }
                }
            })
            .fail(function (result) {
                if (result != null) {
                    /*alert("fail")*/
                }
            })
    });

    //---------------------VALIDAR NOMBRE CALLE-----------------------//
    $("#inputCalle").keyup(function () {

        $.ajax({
            url: "/ValidarCalleDireccion/",
            data:
            {
                calle: $("#inputCalle").val()
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
              //1 correcto
            //-2 cadena vacia
            //-1 caracteres invalidos
            //-3 error metodo o bd
                    switch (result.resultado.toString()) {
                        case "1": //1 todo bien
                            $("#inputCalle").css("background-color", "#ffffff");
                            $("#divAlertCalle").hide("slow");
                            break;

                        case "-1": //-1caracteres ivalidos
                            $("#inputCalle").css("background-color", "#ffffff");
                            $("#divAlertCalle").show("slow");
                            document.getElementById('labelAlertCalle').textContent = "Caracteres invalidos";
                            break;
                        case "-2": //-2 vacio
                            $("#inputCalle").css("background-color", "#ffffff");
                            $("#divAlertCalle").show("slow");
                            document.getElementById('labelAlertCalle').textContent = "Campo no puede quedar vacio";

                            break;
                        case "-3": //-3 error metodo
                            $("#inputCalle").css("background-color", "#ffffff");
                            $("#divAlertCalle").hide("slow");
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
    //---------------------VALIDAR NUMERO EXTERIOR-----------------------//
    $("#inputNumeroExterior").keyup(function () {

        $.ajax({
            url: "/ValidarNumeroExterior/",
            data:
            {
                numero: $("#inputNumeroExterior").val()
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    //1 correcto
                    //-2 cadena vacia
                    //-1 caracteres invalidos
                    //-3 error metodo o bd
                    switch (result.resultado.toString()) {
                        case "1": //1 todo bien
                            $("#inputNumeroExterior").css("background-color", "#ffffff");
                            $("#divAlertNumeroExterior").hide("slow");
                            break;

                        case "-1": //-1caracteres ivalidos
                            $("#inputNumeroExterior").css("background-color", "#ffffff");
                            $("#divAlertNumeroExterior").show("slow");
                            document.getElementById('labelAlertNumeroExterior').textContent = "Caracteres invalidos";
                            break;
                        case "-2": //-2 vacio
                            $("#inputNumeroExterior").css("background-color", "#ffffff");
                            $("#divAlertNumeroExterior").show("slow");
                            document.getElementById('labelAlertNumeroExterior').textContent = "Campo no puede quedar vacio";

                            break;
                        case "-3": //-3 error metodo
                            $("#inputNumeroExterior").css("background-color", "#ffffff");
                            $("#divAlertNumeroExterior").hide("slow");
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

    //---------------------VALIDAR NUMERO INTERIOR-----------------------//
    $("#inputNumeroInterior").keyup(function () {

        $.ajax({
            url: "/ValidarNumeroInterior/",
            data:
            {
                numero: $("#inputNumeroInterior").val()
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    //1 correcto
                    //-2 cadena vacia
                    //-1 caracteres invalidos
                    //-3 error metodo o bd
                    switch (result.resultado.toString()) {
                        case "1": //1 todo bien
                            $("#inputNumeroInterior").css("background-color", "#ffffff");
                            $("#divAlertNumeroInterior").hide("slow");
                            break;

                        case "-1": //-1caracteres invalidos
                            $("#inputNumeroInterior").css("background-color", "#ffffff");
                            $("#divAlertNumeroInterior").show("slow");
                            document.getElementById('labelAlertNumeroInterior').textContent = "Caracteres invalidos";
                            break;
                        case "-2": //-2 vacio
                            $("#inputNumeroInterior").css("background-color", "#ffffff");
                            $("#divAlertNumeroInterior").show("slow");
                            document.getElementById('labelAlertNumeroInterior').textContent = "Campo no puede quedar vacio";

                            break;
                        case "-3": //-3 error metodo
                            $("#inputNumeroInterior").css("background-color", "#ffffff");
                            $("#divAlertNumeroInterior").hide("slow");
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

    //---------------------VALIDAR DESTINATARIO-----------------------//
    $("#inputDestinatario").keyup(function () {

        $.ajax({
            url: "/ValidarDestinatario/",
            data:
            {
                destinatario: $("#inputDestinatario").val()
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    //1 correcto
                    //-2 cadena vacia
                    //-1 caracteres invalidos
                    //-3 error metodo o bd
                    switch (result.resultado.toString()) {
                        case "1": //1 todo bien
                            $("#inputDestinatario").css("background-color", "#ffffff");
                            $("#divAlertDestinatario").hide("slow");
                            break;

                        case "-1": //-1caracteres invalidos
                            $("#inputDestinatario").css("background-color", "#ffffff");
                            $("#divAlertDestinatario").show("slow");
                            document.getElementById('labelAlertDestinatario').textContent = "Caracteres invalidos";
                            break;
                        case "-2": //-2 vacio
                            $("#inputDestinatario").css("background-color", "#ffffff");
                            $("#divAlertDestinatario").show("slow");
                            document.getElementById('labelAlertDestinatario').textContent = "Campo no puede quedar vacio";

                            break;
                        case "-3": //-3 error metodo
                            $("#inputDestinatario").css("background-color", "#ffffff");
                            $("#divAlertDestinatario").hide("slow");
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

var delayTimer;
function doSearch(text) {
   
        clearTimeout(delayTimer);
        delayTimer = setTimeout(function () {
            
                ObtenerColonias(text);
            
        }, 2000);
    
}

function ObtenerColonias(codigo) {
    $.ajax({
        url: "/ObtenerColoniaPorCodigoPostal/",
        data:
        {
            codigo: codigo
        },
        type: "POST"
    })
        .done(function (result) {
            if (result != null) {
                if (result.entro) {
                    if (result.drop == 1)//muestra el drop
                    {
                        document.getElementById("div-contenido-input-item-colonia").innerHTML =` <select id="inputColonia" name="inputColonia" class="form form-control input-txt-item form-select" asp-items="" required style="text-align: center;"> </select>`;
                        
                        $('#inputColonia').empty();
                        result.colonias.forEach(function (item) {
                            LlenarColonias(item, result.colonia);
                        });
                    }
                    else {
                        //muestra el input manual
                        document.getElementById("div-contenido-input-item-colonia").innerHTML = ` <input value="" name="inputColonia" id="inputColonia" type="text" class="input-txt-item" placeholder="Campo obligatorio" required /> `;

                    }
                }
            }


        })
        .fail(function (result) {
            if (result != null) {
                /*alert("fail")*/
            }
        })
}

function LlenarColonias(item, coloniaSeleccionada) {
    //alert("metodo");
    if (item["nombreColonia"] == coloniaSeleccionada)
        document.querySelector('#inputColonia').add(new Option(item["nombreColonia"], item["nombreColonia"], true, true));
    else
        document.querySelector('#inputColonia').add(new Option(item["nombreColonia"], item["nombreColonia"]));
}

function LlenarPaises(item, paisSeleccionado) {
    //alert("metodo");
    if (item["nombrePais"] == paisSeleccionado)
        document.querySelector('#inputPais').add(new Option(item["nombrePais"], item["iso3"], true, true));
    else
        document.querySelector('#inputPais').add(new Option(item["nombrePais"], item["iso3"]));
}

function LlenarEstados(item, estadoSeleccionado) {

    if (item["nombreEstado"] == estadoSeleccionado) {
        //alert(result.estado + "-" + item["text"])
        document.querySelector('#inputEstado').add(new Option(item["nombreEstado"], item["codigoEstado"], true, true));
    }
    else
        document.querySelector('#inputEstado').add(new Option(item["nombreEstado"], item["codigoEstado"]));
}

function LlenarCiudades(item, ciudadSeleccionada) {

    if (item["nombreCiudad"]== ciudadSeleccionada) {
        //alert(result.estado + "-" + item["text"])
        document.querySelector('#inputCiudad').add(new Option(item["nombreCiudad"], item["nombreCiudad"], true, true));
    }
    else
        document.querySelector('#inputCiudad').add(new Option(item["nombreCiudad"], item["nombreCiudad"]));
}