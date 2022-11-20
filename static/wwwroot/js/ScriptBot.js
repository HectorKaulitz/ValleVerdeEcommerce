
var abierto = false;
/* Set the width of the sidebar to 250px (show it) */
function openNav() {
    if (!abierto) {
        //document.getElementById("mySidepanel").style.display = "inherit";
        document.getElementById("mySidepanel").style.width = "100%";
        
        abierto = true;
    }
    else {
        closeNav();
    }
}

/* Set the width of the sidebar to 0 (hide it) */
function closeNav() {
    document.getElementById("mySidepanel").style.width = "0";
    //document.getElementById("mySidepanel").style.display = "none";
    abierto = false;
}