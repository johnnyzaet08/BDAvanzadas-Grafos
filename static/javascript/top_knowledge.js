const socket = io.connect('http://localhost:5000');
socket.on('connect', () => {
    console.log('Connected to server, top_knowledge');
});
let areas_conocimiento = [];
socket.on("topKnowledgeAPI/get", (data) => {
    const tabla = document.getElementById("knowledge");
    const tbody = tabla.getElementsByTagName("tbody")[0];
    data.forEach(element => {
        areas_conocimiento.push(element);
        console.log(element);
        const fila = document.createElement("tr");
        const knowledgeArea = document.createElement("td");
        knowledgeArea.textContent = element.area_conocimiento;
        fila.appendChild(knowledgeArea);

        const projectsQuantity = document.createElement("td");
        projectsQuantity.textContent = element.cantidad_proyectos
        fila.appendChild(projectsQuantity);

        tbody.appendChild(fila);
    });
});

function getTopKnowledge() {
    socket.emit("topKnowledgeAPI");
}