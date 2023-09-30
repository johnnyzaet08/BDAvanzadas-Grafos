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

socket.on('StateDOORS', (doors) => {
    doors.forEach(door => {
      if(door.value){
        document.getElementById(door.target).classList.add('active')
      }else{
        document.getElementById(door.target).classList.remove('active')
      }
    });
});

function loadResearchers_Func() {
    socket.emit('loadResearchers', 'successful');
}

function loadProjects_Func() {
    socket.emit('loadProjects', 'successful');
}

function loadPublications_Func() {
    socket.emit('loadPublications', 'successful');
}

function loadResearchersProj_Func() {
    socket.emit('loadResearchersProj', 'successful');
}

function loadPublicationsProj_Func() {
    socket.emit('loadPublicationsProj', 'successful');
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