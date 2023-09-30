const socket = io.connect('http://localhost:5000');
socket.on('connect', () => {
    console.log('Connected to server, top_institutions');
});
let top_institutions = [];
socket.on("topInstitutionsAPI/get", (data) => {
    console.log(data);
    const tabla = document.getElementById("institution");
    const tbody = tabla.getElementsByTagName("tbody")[0];
    data.forEach(element => {
        top_institutions.push(element);
        console.log(element);
        const fila = document.createElement("tr");
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
    socket.emit("topInstitutionsAPI");
}