const socket = io.connect('http://localhost:5000');
socket.on('connect', () => {
    console.log('Connected to server, search_researchers');
});
let investigator = [{
    "id": "--",
    "nombre_completo": "--",
    "titulo_academico": "--",
    "institucion": "--",
    "email": "--",
    "colegas_de_proyectos": "--"
}];
let selectedInvestigator = null;

socket.on('findColleagueAPI/get', (data) => {
    const select = document.getElementById('investigators');
    const optionElement = document.createElement('option');
    optionElement.value = "--";
    optionElement.text = "--";
    select.appendChild(optionElement);
    data.forEach(element => {
        const optionElement = document.createElement('option');
        optionElement.value = element["nombre_completo"];
        optionElement.text = element["nombre_completo"];
        select.appendChild(optionElement);
        investigator.push(element);
    });
    console.log(investigator);
});


function onSelected() {
    const tabla = document.getElementById("investigator");
    const tbody = tabla.getElementsByTagName("tbody")[0];
    tbody.innerHTML = "";
    selectedInvestigator = document.getElementById("investigators").value;
    if (selectedInvestigator === "--") {
        return;
    }
    const investigator_ = investigator.find(knowledge => knowledge.nombre_completo === selectedInvestigator);
    const fila = document.createElement("tr");

    const id = document.createElement("td");
    id.textContent = investigator_.id;
    fila.appendChild(id);

    const investigator_name = document.createElement("td");
    investigator_name.textContent = investigator_.nombre_completo;
    fila.appendChild(investigator_name);

    const degree = document.createElement("td");
    degree.textContent = investigator_.titulo_academico;
    fila.appendChild(degree);

    const institution = document.createElement("td");
    institution.textContent = investigator_.institucion;
    fila.appendChild(institution);

    const email = document.createElement("td");
    email.textContent = investigator_.email;
    fila.appendChild(email);

    const colleagues = document.createElement("td");
    const list_colleagues = document.createElement("ul");
    investigator_.colegas_de_proyectos.forEach(element => {
        const colleague = document.createElement("li");
        colleague.textContent = element;
        list_colleagues.appendChild(colleague);
    })
    colleagues.appendChild(list_colleagues);
    fila.appendChild(colleagues);

    tbody.appendChild(fila);

}

document.addEventListener('DOMContentLoaded', function() {
    getKnowledge();
    const select = document.getElementById('investigators');
    select.addEventListener('change', onSelected);
});

function getKnowledge() {
    socket.emit("findColleagueAPI");
}

