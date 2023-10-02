const socket = io.connect('http://localhost:5000');
socket.on('connect', () => {
    console.log('Connected to server, associate_article');
});


socket.on('associate_articleAPI', (message) => {
    if(message == "Successful"){
        document.getElementById("myForm").reset();
        alert("Successful");
    }else{
        alert(message);
    }
});

socket.on('publicationsAPI/get', (data) => {
    const select = document.getElementById('publications');
    data.forEach(element => {
        const optionElement = document.createElement('option');
        optionElement.value = element["pu.titulo_publicacion"];
        optionElement.text = element["pu.titulo_publicacion"];
        select.appendChild(optionElement);
    });
});

socket.on('projectsAPI/get', (data) => {
    const select = document.getElementById('projects');
    console.log(data);
    data.forEach(element => {
        const optionElement = document.createElement('option');
        optionElement.value = element["p.titulo_proyecto"];
        optionElement.text = element["p.titulo_proyecto"];
        select.appendChild(optionElement);
    });
});

function addNewResearcher() {
    let publication = document.getElementById("publications").value;
    let project = document.getElementById("projects").value;
    socket.emit("associate_articleAPI/add", publication, project);
};

window.onload = function() {
    var inputs = document.getElementsByClassName('js-input');
    var add_btn = document.getElementById("add-btn");

    socket.emit("publicationsAPI/get")
    socket.emit("projectsAPI/get")

    for (let i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener('change', myfunc);
    };

    add_btn.addEventListener("click", addNewResearcher);

}

function myfunc() {
    if (this.value) {
        this.classList.add('not-empty');
    } else {
        this.classList.remove('not-empty');
    }
}
