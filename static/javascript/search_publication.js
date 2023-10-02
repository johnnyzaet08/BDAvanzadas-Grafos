const socket = io.connect('http://localhost:5000');
socket.on('connect', () => {
    console.log('Connected to server, search_researchers');
});
let researchers = [];
let projects = [];
let selectedResearcher = null;

socket.on("findPublicationByNameAPI/get", (data) => {
    console.log(data);
    const tabla = document.getElementById("publications");
    const tbody = tabla.getElementsByTagName("tbody")[0];
    data.forEach(element => {
        researchers.push(element);
        console.log(element);
        const fila = document.createElement("tr");

        const id = document.createElement("td");
        id.textContent = element.idPub;
        fila.appendChild(id);

        const title = document.createElement("td");
        title.textContent = element.titulo_publicacion;
        fila.appendChild(title);

        const journal = document.createElement("td");
        journal.textContent = element.nombre_revista;
        fila.appendChild(journal);

        const year = document.createElement("td");
        year.textContent = element.anno_publicacion;
        fila.appendChild(year);

        const project = document.createElement("td");
        project.textContent = element.titulo_proyecto;
        fila.appendChild(project);

        tbody.appendChild(fila);
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const nameInput = document.getElementById('name');
    const researcher_projects = document.getElementById("researcher_projects");

    function getPublication() {
        //clear table
        const tabla = document.getElementById("publications");
        const tbody = tabla.getElementsByTagName("tbody")[0];
        tbody.innerHTML = "";
        let researcher = document.getElementById("name").value;
        socket.emit("findPublicationByNameAPI", researcher);
    }

    nameInput.addEventListener('input', getPublication);
});


window.onload = function() {
    var inputs = document.getElementsByClassName('js-input');

    for (let i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener('change', myfunc);
    };

}

function myfunc() {
    if (this.value) {
        this.classList.add('not-empty');
    } else {
        this.classList.remove('not-empty');
    }
}