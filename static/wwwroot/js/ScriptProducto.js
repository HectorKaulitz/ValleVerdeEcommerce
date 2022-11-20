var cx;
var imgExpandida = document.getElementById("imgExpandida");
var img = document.getElementById("imgProductoSeleccionado");
var lente = document.getElementById("divLente");

function CambiarImagenPrincipal(rutaImagen) {
   
    img.src = rutaImagen;
    
    AsignarImagenZoom();

}

function AsignarImagenZoom() {
   

    /* Se calcula el radio entre el lente y la imagen*/
    cx = imgExpandida.offsetWidth / lente.offsetWidth;
    //cy = imgExpandida.offsetHeight / lente.offsetHeight;
    //console.log("w:" + img.width + " h:" + img.height)
    /*Asignamos la imagen con el tamaño del lente*/
    imgExpandida.style.backgroundImage = "url('" + img.src + "')";

    setTimeout(() => {
        //console.log("w2:" + img.width + " h2:" + img.height + " cx:" + cx)
        imgExpandida.style.backgroundSize = (img.width * cx) + "px " + (img.height * cx) + "px";
    }, 50);
}

function AjustarTamanoImagen(e) {
    var contenedorImagen = document.getElementById("idContenedorImagenProducto");

    var ancho = contenedorImagen.clientWidth
    var factorCrecimientoResultado = 1

    if (window.screen.width >= 768) {
        factorCrecimientoResultado = 1.45
    } else {
        factorCrecimientoResultado = 1.2
    }

    contenedorImagen.style.height = ancho + "px";

    lente.style.width = (ancho / 3) + "px";
    lente.style.height = (ancho / 3) + "px";

    imgExpandida.style.width = (ancho * factorCrecimientoResultado) + "px";
    imgExpandida.style.height = (ancho * factorCrecimientoResultado) + "px";

    img.style.maxHeight = (ancho - (20 * 2)) + "px";
    
    var imagenes = document.getElementsByClassName("contenedor-item-seleccion");

    for ( i = 0; i < imagenes.length; i++) {
        ancho = imagenes[i].clientWidth

        imagenes[i].style.height = ancho + "px";
    }
}

$(document).ready(function(){
        
       
    ZoomImagen();
    OcultarZoom(null);

        

    function ZoomImagen() {
        /* Creamos el lente */
        lente = document.createElement("DIV");
        lente.setAttribute("class", "img-zoom-lens");
        lente.setAttribute("id", "divLente");

        /* Lo insertamos en la imagen*/
        img.parentElement.insertBefore(lente, img);

        AsignarImagenZoom();

        /* Eventos de movimiento, mouse dentro y fuera*/
        lente.addEventListener("mousemove", MoverLente);
        img.addEventListener("mousemove", MoverLente);

        lente.addEventListener("touchmove", MoverLente);
        img.addEventListener("touchmove", MoverLente);

        lente.addEventListener("mouseover", MostrarZoom)
        img.addEventListener("mouseover", MostrarZoom)

        lente.addEventListener("mouseout", OcultarZoom)
        img.addEventListener("mouseout", OcultarZoom)

        function MoverLente(e) {
            var pos, x, y;
            /* Prevenir acciones por defecto*/
            e.preventDefault();

            /* Obtener coordenadas del cursor*/
            pos = ObtenerPosicionCursor(e);

            /* Calcula la posicion del lente */
            x = pos.x - (lente.offsetWidth / 2);
            y = pos.y - (lente.offsetHeight / 2);

            /* Verificamos que el lente no este fuera de la imagen */
            if (x > img.width - lente.offsetWidth)
            {
                x = img.width - lente.offsetWidth;
            }
            if (x < 0)
            {
                x = 0;
            }
            if (y > img.height - lente.offsetHeight)
            {
                y = img.height - lente.offsetHeight;
            }
            if (y < 0)
            {
                y = 0;
            }
            /* Asignar la posicion del lente */
            lente.style.left = x + "px";
            lente.style.top = y + "px";

            /* Mostrar la imagen del lente*/
            imgExpandida.style.backgroundPosition = "-" + (x * cx) + "px -" + (y * cx) + "px";
        }

        function ObtenerPosicionCursor(e) {
            var a, x = 0, y = 0;
            e = e || window.event;

            /* Obtiene el x y de la imagen:*/
            a = img.getBoundingClientRect();

            /* Calcula las coordenadas x y relativas a la imagen:*/
            x = e.pageX - a.left;
            y = e.pageY - a.top;

            /*consider any page scrolling:*/
            x = x - window.pageXOffset;
            y = y - window.pageYOffset;
            return { x: x, y: y };
        }
    }

    function OcultarZoom(e) {
        imgExpandida.style.visibility = "hidden"
        lente.style.visibility = "hidden"
    }

    function MostrarZoom(e) {
        imgExpandida.style.visibility = "visible"
        lente.style.visibility = "visible"
    }

    //Para mantener el tamano de la imagen grande
    window.addEventListener('resize', function (event) {
        AjustarTamanoImagen()
        AsignarImagenZoom();
           
    }, true);

    

    //Mandarlo llamar una vez cuando carga la ventana
    setTimeout(() => {
        AjustarTamanoImagen()
        AsignarImagenZoom();
       
    }, 50);
   
    
});

