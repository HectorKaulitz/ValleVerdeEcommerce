function CambiarTipoEnvio (valorR)
{
    //var url = window.location.search;
    //const urlParametros = new URLSearchParams(url);
   // alert("" + idVenta + "-" + " " + valor)
    $.ajax({
        async: false,
        url: "/ValidacionVenta/ActualizarTipoEnvio/",
        data:
        {
            valor: valorR
        },
        type: "POST"
    })
        .done(function (result) {
            if (result != null) {

                window.location.reload();
            }
        })
        .fail(function (result) {
            if (result != null) {
                /*alert("fail")*/
            }
        })
}

function GenerarPagoCompra(idUsuarioEncriptado) {

    var url = window.location.search;
    const urlParametros = new URLSearchParams(url);

    //Generar la venta, despues redirigirlo al lugar correcto

    var status = -1 //1 es finalizada

    $.ajax({
        async: false,
        url: "/ValidacionVenta/CrearVenta/",
        data:
        {
            idUsuarioEncriptado: idUsuarioEncriptado
        },
        type: "POST"
    })
        .done(function (result) {
            if (result != null) {
                if (result.estado == 1) {
                    window.location.replace('' + result.url);
                }
                else {
                    alert("Error crear preferencia")
                }
            }
        })
        .fail(function (result) {
            if (result != null) {
                /*alert("fail")*/
            }
        })


}

function ActualizarTipoPago(idTipoP)
{

    //Si es tipo 1 calcular y mostrarle descuento

    var url = window.location.search;
    
    $.ajax({
        async: false,
        url: "/ValidacionVenta/ActualizarTipoPagoCarrito/",
        data:
        {
            idTipoPago: idTipoP
        },
        type: "POST"
    })
        .done(function (result) {
            if (result != null) {

                window.location.reload();
            }
        })
        .fail(function (result) {
            if (result != null) {
                /*alert("fail")*/
            }
        })
}