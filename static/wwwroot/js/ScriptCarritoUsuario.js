var min = 0;
function ValidarCantidadIngresada(pos, codigo, keycode,idProductoCarrito,idUsu) {
    if ((keycode >= 48 && keycode <= 57) || (keycode >= 96 && keycode <= 105)) {
        var input = document.getElementById("cantidadC " + pos);
        var cant = parseFloat(input.value);
        var existencia = ObtenerExistencia(codigo);
        if (existencia > 0) {

            if (cant > 0) {
                if (cant <= existencia) {//si es mayor a 0
                    input.value = parseFloat(cant);
                }
                else
                {
                    //es mayor a 0 pero es mayor a la existencia
                        input.value = parseFloat(existencia);
                }
            }
            else {
                input.value = 0;
            }
        }
        else {
            input.value = 0;
        }
    }
    ActualizarCantidadBD(idProductoCarrito, document.getElementById("cantidadC " + pos).value, 3, pos, idUsu);
}

function RestarCantidad(pos, codigo, idProductoCarrito, idUsu) {
    var input = document.getElementById("cantidadC " + pos);
    var cant = parseFloat(input.value);
    var cantS = parseInt(cant - 1);
    var existencia = ObtenerExistencia(codigo);
    if (existencia > 0) {
        if (cantS > 0) {
            if (cantS <= existencia) /*la cantidad sigue siendo menor o igual a la existencia*/ {
                input.value = cantS;

            }
            else { /*la cantidad sigue siendo la misma*/
                input.value = cant;
            }
        } else {
            input.value = 0;
        }

    }
    else {
        input.value = 0;
    }
   
    ActualizarCantidadBD(idProductoCarrito, document.getElementById("cantidadC " + pos).value, 3, pos, idUsu);
}

function AumentarCantidad(pos, codigo, idProductoCarrito, idUsu) {
    /* alert(pos);*/
    var input = document.getElementById("cantidadC " + pos);
    var cant = parseFloat(input.value);
    var cantS = parseInt(cant + 1);
    var existencia = ObtenerExistencia(codigo);
    if (existencia > 0) {
        if (cantS > 0) {
            if (cantS <= existencia) /*la cantidad sigue siendo menor o igual a la existencia*/ {
                input.value = cantS;

            }
            else { /*la cantidad sigue siendo la misma*/
                input.value = cant;
            }
        }
        else {
            input.value = 0;
        }

    }
    else {
        input.value = 0;
    }
    ActualizarCantidadBD(idProductoCarrito, document.getElementById("cantidadC " + pos).value, 3, pos, idUsu);
   
}

function ObtenerExistencia(codigoB) {
    var exis = 0;
    $.ajax({
        async: false,
        url: "/ValidacionVenta/ValidarExistenciaProducto/",
        data:
        {
            codigoBarras: codigoB

        },
        type: "POST"
    })
        .done(function (result) {
            if (result != null) {
                /* alert(JSON.stringify(result));*/

                exis = result.resultado;

            }
        })
        .fail(function (result) {
            if (result != null) {
                /*alert("fail")*/
            }
        })

    return exis;
}

function EliminarProductoCarrito(idProductoCar) {
    $.ajax({
        async: false,
        url: "/ValidacionVenta/EliminarProductoDelCarrito/",
        data:
        {
            idProductoCarrito: idProductoCar

        },
        type: "POST"
    })
        .done(function (result) {
            if (result != null) {
                /* alert(JSON.stringify(result));*/
                if (result.resultado == 1) {
                    ActualizarCarritoCompletoVisualC();
                   // ActualizarFavoritosVisual();

                }
            }
        })
        .fail(function (result) {
            if (result != null) {
                /*alert("fail")*/
            }
        })
}

function ActualizarCantidadBD(idProductoC,cant,tip,ind,idUs) {
    $.ajax({
        async: false,
        url: "/ValidacionVenta/ActualizarCantidadProductoCarrito/",
        data:
        {
            idProductoCarrito: idProductoC,
            cantidad:cant,
            tipo: tip,
            idUsuario: idUs

        },
        type: "POST"
    })
        .done(function (result) {
            if (result != null) {
                 //alert(JSON.stringify(result));
                document.getElementById('precioT ' + ind).textContent = "$ " + result.resultado.totalPrecioProducto;
                var exist = parseFloat(result.resultado.existencia);
                if (exist < 0) {
                    document.getElementById('labelAlert ' + ind).textContent = "Existencia:" + 0;
                }
                else {
                    document.getElementById('labelAlert ' + ind).textContent = "Existencia:" + exist;
                }
                ActualizarTotalesC();
                //document.getElementById('idSubTotal').textContent = "$ "+result.total.totalSinEnvio;
                //document.getElementById('idEnvio').textContent = "$ " +result.total.envio;
                //document.getElementById('idTotal').textContent = "$ " + result.total.totalConEnvio;
                

            }
        })
        .fail(function (result) {
            if (result != null) {
                /*alert("fail")*/
            }
        })
    
}
function ActualizarCarritoCompletoVisualC() {
    $('#carrito').load('/Venta/ObtenerCarritoUsuario')
}
function ActualizarFavoritosVisualC() {
    $('#favoritos').load('/Venta/ObtenerFavoritosUsuario')
}
function ActualizarTotalesC() {
    //alert("entro");
    $('#totalesC').load('/Venta/ObtenerTotalesCarrito');
}
$(document).ready(function ()
{

});