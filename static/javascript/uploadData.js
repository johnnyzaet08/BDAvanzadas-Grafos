const urlParams = new URLSearchParams(window.location.search);
const message = urlParams.get('message');
if (message) {
    alert(message);
}

const socket = io.connect('http://localhost:5000');
socket.on('connect', () => {
    socket.emit('connectState', 'successful');
    console.log('Connected to server');
});

socket.on('uploadMessage', (message) => {
    alert(message);
})

function loadResearchers_Func() {
    file = document.getElementById("load_researchers").files[0];
    socket.emit('loadResearchers', file);
}

function loadProjects_Func() {
    file = document.getElementById("load_proj").files[0]
    socket.emit('loadProjects',file);
}

function loadPublications_Func() {
    file = document.getElementById("load_pub").files[0]
    socket.emit('loadPublications', file);
}

function loadResearchersProj_Func() {
    file = document.getElementById("load_researchers-proj").files[0]
    socket.emit('loadResearchersProj', file);
}

function loadPublicationsProj_Func() {
    file = document.getElementById("load_pub-proj").files[0]
    socket.emit('loadPublicationsProj', file);
}

window.onload = function(){

    var loadResearchers = document.getElementById('loadResearchers');
    var loadProjects = document.getElementById('loadProjects');
    var loadPublications = document.getElementById('loadPublications');
    var loadResearchersProj = document.getElementById('loadResearchersProj');
    var loadPublicationsProj = document.getElementById('loadPublicationsProj');


    loadResearchers.addEventListener("click", loadResearchers_Func);
    loadProjects.addEventListener("click", loadProjects_Func);
    loadPublications.addEventListener("click", loadPublications_Func);
    loadResearchersProj.addEventListener("click", loadResearchersProj_Func);
    loadPublicationsProj.addEventListener("click", loadPublicationsProj_Func);

 }