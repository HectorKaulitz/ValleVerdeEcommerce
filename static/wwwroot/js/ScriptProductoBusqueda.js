var numeroToast = 0

function ActualizarCarritoVisual() {
    //$.get('/Inicio/ObtenerCarritoFlotante', function (data) {
    //    $('#contenedor-carrito-flotante').html(data.getElementById("contenedor-carrito-flotante"));
    //});

    $('#contenedor-carrito-flotante').load('/Inicio/ObtenerCarritoFlotante');
    

}
function ActualizarNotificacionVisual() {
    //$.get('/Inicio/ObtenerCarritoFlotante', function (data) {
    //    $('#contenedor-carrito-flotante').html(data.getElementById("contenedor-carrito-flotante"));
    //});

    $('#contenedor-login').load('/Sesion/ContenedorUsuario')
    $('#contenedor-loginF').load('/Sesion/ContenedorUsuario')

}
function AgregarAcarrito(idProd, idUsu,urlImagen, nombre)
{
    /*alert("entro");*/
    if (idUsu != null) {
        $.ajax({
            async: false,
            url: "/ValidacionVenta/AgregarProductoCarrito/",
            data:
            {
                idUsuario: idUsu,
                idProducto: idProd,
                cantidad: 1

            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {

                    if (result.resultado > 0) {
                        /* alert(JSON.stringify(result));*/

                        //alert(result.resultado + "  "+result.mensaje)
                        //Crear la alerta, agregarla y luego mostrarla
                        var contenedor = document.getElementById("alertas")

                        //Eliminar los que ya se ocultaron
                        var listaToast = [].slice.call(contenedor.querySelectorAll('.toast'))


                        listaToast.forEach(element => {
                            if (element.classList.contains("hide")) {
                                contenedor.removeChild(element)
                            }
                        })

                        contenedor.innerHTML += `<div id='toast` + numeroToast + `' class='toast' role='alert' aria-live='assertive' aria-atomic='true'>
                                                <div class='toast-header' >
                                                  <img src='` + urlImagen + `' class='rounded me-2 img-fluid' alt='` + nombre + `'>
                                                  <strong class='me-auto'> ` + nombre + `</strong>
                                                  <small class='text-muted'>Justo ahora</small>
                                                  <button type='button' class='btn-close' data-bs-dismiss='toast' aria-label='Close'></button>
                                                </div>
                                                <div class='toast-body'>
                                                    Agregado al carrito
                                                </div>
                                              </div > `

                        var toastElList = [].slice.call(document.querySelectorAll('.toast'))
                        var toastList = toastElList.map(function (toastEl) {
                            // Creates an array of toasts (it only initializes them)
                            return new bootstrap.Toast(toastEl) // No need for options; use the default options
                        });

                        toastList.forEach(toast => {
                            toast.show()
                        }); // This show them

                        //var t = new bootstrap.Toast(document.getElementById("toast" + numeroToast))

                        //t.show()

                        numeroToast += 1
                    }
                    else {
                        alert('No se pudo agregar '+nombre+ ' al carrito por: '+result.mensaje)
                    }

                    ActualizarCarritoVisual();
                }
            })
            .fail(function (result) {
                if (result != null) {
                    alert("No se agrego al carrito: "+ JSON.stringify(result))
                }
            })
    }
    else {
        alert("No se agrego al carrito por que no esta iniciado sesion")
    }
}

function AgregarFavoritos(idProduc,idUsua,imagen,nombre) {
    //alert("entro");
    if (idUsua != null) {
        $.ajax({
            async: false,
            url: "/ValidacionVenta/AgregarProductoFavorito/",
            data:
            {
                idUsuario: idUsua,
                idProducto: idProduc

            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
                    /* alert(JSON.stringify(result));*/
                    if (result.resultado > 0) {
                        ActualizarNotificacionVisual();
                        var contenedor = document.getElementById("alertas")

                        ////Eliminar los que ya se ocultaron
                        var listaToast = [].slice.call(contenedor.querySelectorAll('.toast'))


                        listaToast.forEach(element => {
                            if (element.classList.contains("hide")) {
                                contenedor.removeChild(element)
                            }
                        })

                        if (document.getElementById("'fav" + idProduc + "'").classList.contains('estaFavorito')) {
                            document.getElementById("'fav" + idProduc + "'").classList.remove('estaFavorito');
                            document.getElementById("'fav" + idProduc + "'").classList.remove('fa-solid');
                            document.getElementById("'fav" + idProduc + "'").classList.add('fa-regular');

                            contenedor.innerHTML += `<div id='toast` + numeroToast + `' class='toast' role='alert' aria-live='assertive' aria-atomic='true'>
                                                    <div class='toast-header' >
                                                      <img src='` + imagen + `' class='rounded me-2 img-fluid' alt='` + nombre + `'>
                                                      <strong class='me-auto'> ` + nombre + `</strong>
                                                      <small class='text-muted'>Justo ahora</small>
                                                      <button type='button' class='btn-close' data-bs-dismiss='toast' aria-label='Close'></button>
                                                    </div>
                                                    <div class='toast-body'>
                                                        Eliminado de favorito
                                                    </div>
                                                  </div > `;
                        }
                        else {
                            document.getElementById("'fav" + idProduc + "'").classList.add('estaFavorito');
                            document.getElementById("'fav" + idProduc + "'").classList.remove('fa-regular');
                            document.getElementById("'fav" + idProduc + "'").classList.add('fa-solid');

                            contenedor.innerHTML += `<div id='toast` + numeroToast + `' class='toast' role='alert' aria-live='assertive' aria-atomic='true'>
                                                    <div class='toast-header' >
                                                      <img src='` + imagen + `' class='rounded me-2 img-fluid' alt='` + nombre + `'>
                                                      <strong class='me-auto'> ` + nombre + `</strong>
                                                      <small class='text-muted'>Justo ahora</small>
                                                      <button type='button' class='btn-close' data-bs-dismiss='toast' aria-label='Close'></button>
                                                    </div>
                                                    <div class='toast-body'>
                                                        Agregado a favorito
                                                    </div>
                                                  </div > `;
                        }





                        var toastElList = [].slice.call(document.querySelectorAll('.toast'))
                        var toastList = toastElList.map(function (toastEl) {
                            // Creates an array of toasts (it only initializes them)
                            return new bootstrap.Toast(toastEl) // No need for options; use the default options
                        });

                        toastList.forEach(toast => {
                            toast.show()
                        }); // This show them

                        //var t = new bootstrap.Toast(document.getElementById("toast" + numeroToast))

                        //t.show()

                        numeroToast += 1

                        // alert(result.resultado + "  "+result.mensaje)

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
