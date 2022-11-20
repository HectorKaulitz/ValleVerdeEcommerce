

function ObtenerProductosVenta(idVenta, idContenedor, idBoton) {

    var contenedor = document.getElementById(idContenedor);

    var contenedorCargando = contenedor.querySelector("#cargando");

    var boton = document.getElementById(idBoton)

    if (contenedorCargando != null) {
        $('#' + idContenedor).load('/Venta/ProductosVentaHistorial?idVentaEncriptado=' + idVenta)
    }
  
    //Ver si esta expandido o no
    if (boton.classList.contains("collapsed")) {
        boton.innerHTML = "Ver detalles compra<i class='fa-solid fa-chevron-down'></i>";
    } else {
        boton.innerHTML = "Ocultar detalles compra<i class='fa-solid fa-chevron-up'></i>";
    }

}

function CancelarVenta(idVent) {
    $.ajax({
        url: "/ValidacionVenta/CancelarVentaUsuario/",
        data:
        {
            idVenta:idVent

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


$(document).ready(function(){
        
       
    
    
});

