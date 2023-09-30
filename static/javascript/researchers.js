const socket = io.connect('http://localhost:5000');
socket.on('connect', () => {
    console.log('Connected to server, researchers');
});


socket.on('researchersAPI', (message) => {
    if(message == "Successful"){
        document.getElementById("myForm").reset();
        alert("Successful")
    }else{
        alert(message);
    }
});

function addNewResearcher() {
    let name = document.getElementById("name").value;
    let degree = document.getElementById("degree").value;
    let email = document.getElementById("email").value;
    let institution = document.getElementById("institution").value;
    socket.emit("researchersAPI/add", name, degree, institution, email);
};

function updateResearcher() {
    let id = document.getElementById("id").value;
    if(id == null || id == ""){
        return alert("Ingrese el ID");
    }
    let name = document.getElementById("name").value;
    let degree = document.getElementById("degree").value;
    let email = document.getElementById("email").value;
    let institution = document.getElementById("institution").value;
    socket.emit("researchersAPI/update", id, name, degree, institution, email);
};

window.onload = function() {
    var inputs = document.getElementsByClassName('js-input');
    var add_btn = document.getElementById("add-btn");
    var update_btn = document.getElementById("update-btn");

    for (let i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener('change', myfunc)
    };

    add_btn.addEventListener("click", addNewResearcher)
    update_btn.addEventListener("click", updateResearcher)

}



function myfunc() {
    if (this.value) {
        this.classList.add('not-empty');
    } else {
        this.classList.remove('not-empty');
    }
}
