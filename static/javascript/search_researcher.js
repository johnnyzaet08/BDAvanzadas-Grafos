const socket = io.connect('http://localhost:5000');
socket.on('connect', () => {
    console.log('Connected to server, search_researchers');
});
let researchers = [];
let projects = [];
let selectedResearcher = null;

socket.on("findResearcherByNameAPI/get", (data) => {
    console.log(data);
    const tabla = document.getElementById("researcher");
    const tbody = tabla.getElementsByTagName("tbody")[0];
    data.forEach(element => {
        researchers.push(element);
        console.log(element);
        const fila = document.createElement("tr");
        fila.id = element.id;
        fila.onclick = function() {
            const researcher = researchers.find(researcher => researcher.id === element.id);
            projects = researcher.proyectos;
            selectedResearcher = researcher.nombre_completo;
            getProjects();
        }

        const id = document.createElement("td");
        id.textContent = element.id;
        fila.appendChild(id);

        const name = document.createElement("td");
        name.textContent = element.nombre_completo;
        fila.appendChild(name);

        const degree = document.createElement("td");
        degree.textContent = element.titulo_academico;
        fila.appendChild(degree);

        const institution = document.createElement("td");
        institution.textContent = element.institucion;
        fila.appendChild(institution);

        const email = document.createElement("td");
        email.textContent = element.email
        fila.appendChild(email);

        tbody.appendChild(fila);
    });
});

getProjects = function() {
    const researcher_projects = document.getElementById("researcher_projects");
    researcher_projects.textContent = `${selectedResearcher} has the following projects:`;
    const projects_table = document.getElementById("projects");
    const tbody = projects_table.getElementsByTagName("tbody")[0];
    tbody.innerHTML = "";
    projects_table.style.display = "block";

    projects.forEach(element => {
        const fila = document.createElement("tr");

        const id = document.createElement("td");
        id.textContent = element.idPry;
        fila.appendChild(id);

        const title = document.createElement("td");
        title.textContent = element.titulo_proyecto;
        fila.appendChild(title);

        const knowledge = document.createElement("td");
        knowledge.textContent = element.area_conocimiento;
        fila.appendChild(knowledge);

        const duration = document.createElement("td");
        duration.textContent = element.duracion_meses + " months";
        fila.appendChild(duration);

        const start_year = document.createElement("td");
        start_year.textContent = element.anno_inicio;
        fila.appendChild(start_year);

        tbody.appendChild(fila);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const nameInput = document.getElementById('name');
    const researcher_projects = document.getElementById("researcher_projects");

    function getResearcher() {
        // Clear projects
        researcher_projects.textContent = ``;
        const projects_table = document.getElementById("projects");
        projects_table.style.display = "none";
        const body = projects_table.getElementsByTagName("tbody")[0];
        body.innerHTML = "";
        projects = [];
        //clear table
        const tabla = document.getElementById("researcher");
        const tbody = tabla.getElementsByTagName("tbody")[0];
        tbody.innerHTML = "";
        let researcher = document.getElementById("name").value;
        socket.emit("findResearcherByNameAPI", researcher);
    }

    nameInput.addEventListener('input', getResearcher);
});