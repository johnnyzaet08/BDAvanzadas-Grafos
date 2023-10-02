const socket = io.connect('http://localhost:5000');
socket.on('connect', () => {
    console.log('Connected to server, search_researchers');
});
let knowledge = [{
    "area_conocimiento": "--",
    "TItulos_de_Proyectos": "--",
    "Titulos_de_Publicaciones": "--"
}];
let selectedKnowledge = null;

socket.on('findKnowledgeAPI/get', (data) => {
    const select = document.getElementById('knowledge_area');
    const optionElement = document.createElement('option');
    optionElement.value = "--";
    optionElement.text = "--";
    select.appendChild(optionElement);
    data.forEach(element => {
        const optionElement = document.createElement('option');
        optionElement.value = element["area_conocimiento"];
        optionElement.text = element["area_conocimiento"];
        select.appendChild(optionElement);
        knowledge.push(element);
    });
    console.log(knowledge);
});


function onSelected() {
    const tabla = document.getElementById("knowledge");
    const tbody = tabla.getElementsByTagName("tbody")[0];
    tbody.innerHTML = "";
    selectedKnowledge = document.getElementById("knowledge_area").value;
    if (selectedKnowledge === "--") {
        return;
    }
    const knowledge_area = knowledge.find(knowledge => knowledge.area_conocimiento === selectedKnowledge);
    const fila = document.createElement("tr");

    const knowledge_area_name = document.createElement("td");
    knowledge_area_name.textContent = knowledge_area.area_conocimiento;
    fila.appendChild(knowledge_area_name);

    const projects = document.createElement("td");
    const list_projects = document.createElement("ul");
    knowledge_area.TItulos_de_Proyectos.forEach(element => {
        const project = document.createElement("li");
        project.textContent = element;
        list_projects.appendChild(project);
    })
    projects.appendChild(list_projects);
    fila.appendChild(projects);

    const publications = document.createElement("td");
    const list_publications = document.createElement("ul");
    knowledge_area.Titulos_de_Publicaciones.forEach(element => {
        const publication = document.createElement("li");
        publication.textContent = element;
        list_publications.appendChild(publication);
    })
    publications.appendChild(list_publications);
    fila.appendChild(publications);

    tbody.appendChild(fila);

}

document.addEventListener('DOMContentLoaded', function() {
    getKnowledge();
    const select = document.getElementById('knowledge_area');
    select.addEventListener('change', onSelected);
});

function getKnowledge() {
    socket.emit("findKnowledgeAPI");
}

