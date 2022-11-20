function convertirProductoFavorito(idProductoFav) {
    $.ajax({
        async: false,
        url: "/ValidacionVenta/ConvertirProductoDeFavoritoACarrito/",
        data:
        {
            idProductoFavorito: idProductoFav

        },
        type: "POST"
    })
        .done(function (result) {
            if (result != null) {
                if (result.resultado[0] != "-1") {
                    ActualizarCarritoCompletoVisual();
                    ActualizarFavoritosVisual();
                }
                else {
                    alert("" + result.resultado[1])
                }
            }
        })
        .fail(function (result) {
            if (result != null) {
                /*alert("fail")*/
            }
        })
}
function EliminarProductoFavorito(idProductoFavorit) {
    $.ajax({
        async: false,
        url: "/ValidacionVenta/EliminarProductoDeFavoritos/",
        data:
        {
            idProductoFavorito: idProductoFavorit

        },
        type: "POST"
    })
        .done(function (result) {
            if (result != null) {
                /* alert(JSON.stringify(result));*/
                if (result.resultado == 1) {
                    ActualizarFavoritosVisual();
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


function ActualizarCarritoCompletoVisual() {
    $('#carrito').load('/Venta/ObtenerCarritoUsuario')
}
function ActualizarFavoritosVisual() {
    $('#favoritos').load('/Venta/ObtenerFavoritosUsuario')
}