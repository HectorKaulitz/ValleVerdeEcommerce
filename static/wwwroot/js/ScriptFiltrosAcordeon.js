
function ObtenerSubFiltros(tipoCategoria, id, idContenedor, rutaEncriptada) {
    
    var contenedor = document.getElementById(idContenedor);

    var contenedorCargando = contenedor.querySelector("#cargando");


    if (contenedorCargando != null) {
        $('#' + idContenedor).load('/Inicio/ObtenerSubFiltros?tipoCategoria=' + tipoCategoria + '&id=' + id + '&rutaEncriptada=' + rutaEncriptada)
    }
  
}


$(document).ready(function(){
        
       
    
    
});

