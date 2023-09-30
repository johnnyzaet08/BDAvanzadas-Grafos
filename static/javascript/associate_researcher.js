const socket = io.connect('http://localhost:5000');
socket.on('connect', () => {
    console.log('Connected to server, associate_researcher');
});


socket.on('associate_researcherAPI', (message) => {
    if(message == "Successful"){
        document.getElementById("myForm").reset();
        alert("Successful");
    }else{
        alert(message);
    }
});

socket.on('researchersAPI/get', (data) => {
    const select = document.getElementById('researchers');
    data.forEach(element => {
        const optionElement = document.createElement('option');
        optionElement.value = element["i.Nombre"];
        optionElement.text = element["i.Nombre"];
        select.appendChild(optionElement);
    });
});

socket.on('projectsAPI/get', (data) => {
    const select = document.getElementById('projects');
    data.forEach(element => {
        const optionElement = document.createElement('option');
        optionElement.value = element["p.Titulo"];
        optionElement.text = element["p.Titulo"];
        select.appendChild(optionElement);
    });
});

function addNewResearcher() {
    let researcher = document.getElementById("researchers").value;
    let project = document.getElementById("projects").value;
    socket.emit("associate_researcherAPI/add", researcher, project);
};

function updateResearcher() {
    let id = document.getElementById("id").value;
    if(id == null || id == ""){
        return alert("Ingrese el ID");
    }
    let researcher = document.getElementById("researchers").value;
    let project = document.getElementById("projects").value;
    //socket.emit("associate_researcherAPI/update", id, researcher, project);
};

window.onload = function() {
    var inputs = document.getElementsByClassName('js-input');
    var add_btn = document.getElementById("add-btn");
    var update_btn = document.getElementById("update-btn");

    socket.emit("researchersAPI/get")
    socket.emit("projectsAPI/get")

    for (let i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener('change', myfunc);
    };

    add_btn.addEventListener("click", addNewResearcher);
    update_btn.addEventListener("click", updateResearcher);

}

function myfunc() {
    if (this.value) {
        this.classList.add('not-empty');
    } else {
        this.classList.remove('not-empty');
    }
}
