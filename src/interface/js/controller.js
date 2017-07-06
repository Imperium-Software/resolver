let net = require('net');
const {dialog} = require('electron').remote;

let HOST = 'rainmaker.wunderground.com';
let PORT = 23;

// Get pointers to critical elements
// let test_request = document.getElementById('test-request');
// let test_relay = document.getElementById('test-relay');
// let host_field = document.getElementById('host-field')
// let port_field = document.getElementById('port-field')

// // Add event listeners
// test_request.addEventListener('click', () => {
//   let client = net.Socket();

//   HOST = host_field.value;
//   PORT = port_field.value;

//   client.connect(PORT, HOST, function() {
//     console.log('CONNECTED TO: ' + HOST + ':' + PORT);
//     // Write a message to the socket as soon as the client is connected, the server will receive it as message from the client

//     client.write('Hello from Electron interface!\n#\n')
//   });

//   client.on('data', function(data) {

//     test_relay.value += data;
//     // Close the client socket completely
//     client.destroy();
//   });

//   // Add a 'close' event handler for the client socket
//   client.on('close', function() {
//     console.log('Connection closed');
//   });
// });



document.getElementById('open-file').addEventListener('click', () => {
  dialog.showOpenDialog((filename) => {
    if (filename === undefined) {
      console.log('The user did not select a location to open.')
      return
    }
    console.log(filename)
    fs.readFile(filename[0], 'utf8', (err, data) => {
      if (err) {
        console.log(err)
        return
      }
      editor.value = data;
      toggle_hex = false;
    })
  })
})

// Side Nav

 $(".button-collapse").sideNav();

 $('.button-collapse').sideNav({
      menuWidth: 300, // Default is 300
      edge: 'left', // Choose the horizontal origin
      closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor
      draggable: true, // Choose whether you can drag to open on touch screens,
      //onOpen: function(el) { /* Do Stuff* / }, // A function to be called when sideNav is opened
      //onClose: function(el) { /* Do Stuff* / }, // A function to be called when sideNav is closed
    }
  );

 // Progress Circle

 $('#circle').circleProgress({
    value: 0.75,
    size: 80,
    fill: {
      gradient: ["purple", "blue"]
    }
  }).on('circle-animation-progress', function(event, progress) {
    $(this).find('strong').html(Math.round(100 * progress) + '<i>%</i>');
  });