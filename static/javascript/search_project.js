const socket = io.connect('http://localhost:5000');
socket.on('connect', () => {
    console.log('Connected to server, search_researchers');
});
let researchers = [];
let projects = [];
let publications = [];
let selectedProject = null;

socket.on("findProjectByNameAPI/get", (data) => {
    console.log(data);
    const tabla = document.getElementById("projects");
    const tbody = tabla.getElementsByTagName("tbody")[0];
    data.forEach(element => {
        projects.push(element);
        console.log(element);
        const fila = document.createElement("tr");
        fila.id = element.idPry;
        fila.onclick = function() {
            const project = projects.find(project => project.idPry === element.idPry);
            researchers = project.investigadores;
            publications = project.publicaciones;
            selectedProject = project.titulo_proyecto;
            getResearchers();
            getPublications();
        }

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
});

getResearchers = function() {
    const researcher_projects = document.getElementById("researcher_projects");
    researcher_projects.textContent = `${selectedProject} has the following researchers:`;
    const researchers_table = document.getElementById("researchers");
    const tbody = researchers_table.getElementsByTagName("tbody")[0];
    tbody.innerHTML = "";
    researchers_table.style.display = "block";
    console.log(researchers);
    console.log(selectedProject)
    researchers.forEach(element => {
        const fila = document.createElement("tr");

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
}

getPublications = function() {
    const publication_projects = document.getElementById("publication_projects");
    publication_projects.textContent = `${selectedProject} has the following publications:`;
    const publications_table = document.getElementById("publications");
    const tbody = publications_table.getElementsByTagName("tbody")[0];
    tbody.innerHTML = "";
    publications_table.style.display = "block";
    console.log(publications);
    console.log(selectedProject)
    publications.forEach(element => {
        const fila = document.createElement("tr");

        const title = document.createElement("td");
        title.textContent = element.titulo_publicacion;
        fila.appendChild(title);

        const journal = document.createElement("td");
        journal.textContent = element.nombre_revista;
        fila.appendChild(journal);

        const year = document.createElement("td");
        year.textContent = element.anno_publicacion;
        fila.appendChild(year);



        tbody.appendChild(fila);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const nameInput = document.getElementById('name');
    const researcher_projects = document.getElementById("researcher_projects");

    function getProject() {
        // Clear researchers
        researcher_projects.textContent = ``;
        const researchers_table = document.getElementById("researchers");
        researchers_table.style.display = "none";
        const body = researchers_table.getElementsByTagName("tbody")[0];
        body.innerHTML = "";
        projects = [];

        // Clear publications
        const publication_projects = document.getElementById("publication_projects");
        publication_projects.textContent = ``;
        const publications_table = document.getElementById("publications");
        publications_table.style.display = "none";
        const body2 = publications_table.getElementsByTagName("tbody")[0];
        body2.innerHTML = "";
        publications = [];

        //clear table
        const tabla = document.getElementById("projects");
        const tbody = tabla.getElementsByTagName("tbody")[0];
        tbody.innerHTML = "";
        let researcher = document.getElementById("name").value;
        socket.emit("findProjectByNameAPI", researcher);
    }

    nameInput.addEventListener('input', getProject);
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