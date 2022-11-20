

$(document).ready(function () {

    // Get the input field
    var input = document.getElementById("inputBarraBusqueda");

    // Execute a function when the user presses a key on the keyboard
    if (input != null) {
        input.addEventListener("keypress", function (event) {
            // If the user presses the "Enter" key on the keyboard
            if (event.key === "Enter") {
                // Cancel the default action, if needed
                event.preventDefault();
                // Trigger the button element with a click
                document.getElementById("btnBusqueda").click();
            }
        });

        const ac = new Autocomplete(document.getElementById("inputBarraBusqueda"), {
            data: [{ label: "I'm a label", value: 42 }],
            maximumItems: 5,
            threshold: 1,
            label: 'nombre',
            value: 'idProducto',
            onSelectItem: ({ label, value }) => {
                document.getElementById("btnBusqueda").click();
                console.log("user selected:", label, value);
            }, onInput: (value) => {

                $.ajax({
                    url: "/Producto/ObtenerSugerenciasBusqueda/",
                    data:
                    {
                        busqueda: value
                    },
                    type: "POST"
                })
                    .done(function (result) {
                        if (result != null) {

                            ac.setData(result)

                        }
                    })
                    .fail(function (result) {
                        if (result != null) {
                            /*alert("fail")*/
                        }
                    })



                //var datasrc = [
                //    { label: 'Option 1', value: 'opt1' },
                //    { label: 'Option 2', value: 'opt2' },
                //    { label: 'Option 3', value: 'opt3' },
                //    // ...
                //]

                //ac.setData(datasrc)
            }
        });
    }
    //BOTON BUSQUEDA//
    $("#btnBusqueda").click(function () {

        $.ajax({
            url: "/Validacion/ValidarBusqueda/",
            data:
            {

                busqueda: $("#inputBarraBusqueda").val().toString(),
                
            },
            type: "POST"
        })
            .done(function (result) {
                if (result != null) {
               
                    switch (result.resultado.toString()) {
                        case "1"://todo correcto
                            var form = document.getElementById("formularioBarraBusqueda");
                            window.location.replace('/Productos?tipo='+result.tipo+'&numeroPagina=$1&productosPag='+result.numero+'&busqueda=' + $("#inputBarraBusqueda").val().toString());
                            ////form.setAttribute('asp-route-busqueda=', $("#inputBarraBusqueda").val().toString())
                            //form.submit();
                            break;
                       
                        default:
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