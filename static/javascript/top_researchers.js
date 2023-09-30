const socket = io.connect('http://localhost:5000');
socket.on('connect', () => {
    console.log('Connected to server, top_researchers');
});
let top_researchers = [];
socket.on("topResearchersAPI/get", (data) => {
    console.log(data);
    const tabla = document.getElementById("researchers");
    const tbody = tabla.getElementsByTagName("tbody")[0];
    data.forEach(element => {
        top_researchers.push(element);
        console.log(element);
        const fila = document.createElement("tr");

        const name = document.createElement("td");
        name.textContent = element.nombre_completo;
        fila.appendChild(name);

        const institution = document.createElement("td");
        institution.textContent = element.institucion;
        fila.appendChild(institution);

        const projectsQuantity = document.createElement("td");
        projectsQuantity.textContent = element.cantidad_proyectos
        fila.appendChild(projectsQuantity);

        tbody.appendChild(fila);
    });
});

function getTopInstitutions() {
    socket.emit("topResearchersAPI");
}