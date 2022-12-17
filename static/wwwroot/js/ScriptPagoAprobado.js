function DescargarComprobante() {
    //html2canvas(document.body, {
    //    onrendered: function (canvas) {
    //        document.location = canvas.toDataURL("image/png");
    //    }
    //});

    html2canvas(document.querySelector("#comprobante-pago")).then(canvas => {
        //document.body.appendChild(canvas)

        var link = document.createElement("a");
        link.download = "ComprobantePagoValleVerde.png";
        link.href = canvas.toDataURL();
        link.target = "_blank";
        link.click();

    });
}

function RetomarPago(idVentaEncriptado) {
    //Pago en MercadoPago
    $.ajax({
        async: false,
        url: "/RetomarPago/",
        data:
        {
            idVentaEncriptado: idVentaEncriptado

        },
        type: "POST"
    })
        .done(function (result) {
            if (result != null) {
                if (result.estado == 1) {
                    window.location.replace('' + result.url);
                }
                else {
                    alert("Error al obtener preferencia")
                }
            }
        })
        .fail(function (result) {
            if (result != null) {
                /*alert("fail")*/
            }
        })
}


$(document).ready(function(){
        
       
    
    
});

