const socket = io.connect('http://localhost:5000');
socket.on('connect', () => {
    console.log('Connected to server, publications');
});


socket.on('publicationsAPI', (message) => {
    if(message == "Successful"){
        document.getElementById("myForm").reset();
        alert("Successful");
    }else{
        alert(message);
    }
});

function addNewResearcher() {
    let title = document.getElementById("title").value;
    let year = document.getElementById("year").value;
    let journal = document.getElementById("journal").value;
    socket.emit("publicationsAPI/add", title, year, journal);
};

function updateResearcher() {
    let id = document.getElementById("id").value;
    if(id == null || id == ""){
        return alert("Ingrese el ID");
    }
    let title = document.getElementById("title").value;
    let year = document.getElementById("year").value;
    let journal = document.getElementById("journal").value;
    socket.emit("publicationsAPI/update", id, title, year, journal);
};

window.onload = function() {
    var inputs = document.getElementsByClassName('js-input');
    var add_btn = document.getElementById("add-btn");
    var update_btn = document.getElementById("update-btn");

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
