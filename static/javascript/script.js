
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