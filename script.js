function toggleCheckbox(element) {
    var xhr = new XMLHttpRequest();
    if (element.checked) {
        xhr.open("GET", "/update?output=" + element.id + "&state=1", true)
    } else {
        xhr.open("GET", "/update?output=" + element.id + "&state=0", true)
    }
    xhr.send();
}

async function actualizarBoton() {
    try {
        const response = await fetch('/input', {cache: "no-store"});
        const estado = (await response.text()).trim();
        document.getElementById("indicador").classList.toggle("activo", estado === "1")
        console.log(estado)
    } catch(error) {
        console.error("error al actualizar boton:", error)
    }
    setTimeout(actualizarBoton, 250);
}

actualizarBoton();