function Colapse(cadena, id)
{
    //colapsado = !colapsado;

    if (document.getElementById(cadena+" " + id).classList.contains('fa-square-caret-up')) {
        document.getElementById(cadena +" " + id).classList.remove('fa-square-caret-up');
        document.getElementById(cadena +" " + id).classList.add('fa-square-caret-down');
    }
    else {
        document.getElementById(cadena +" " + id).classList.remove('fa-square-caret-down');
        document.getElementById(cadena +" " + id).classList.add('fa-square-caret-up');
    }
}