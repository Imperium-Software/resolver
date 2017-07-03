let net = require('net');

let HOST = 'rainmaker.wunderground.com';
let PORT = 23;

// Get pointers to critical elements
let test_request = document.getElementById('test-request');
let test_relay = document.getElementById('test-relay');
let host_field = document.getElementById('host-field')
let port_field = document.getElementById('port-field')

// Add event listeners
test_request.addEventListener('click', () => {
  let client = net.Socket();

  HOST = host_field.value;
  PORT = port_field.value;

  client.connect(PORT, HOST, function() {
    console.log('CONNECTED TO: ' + HOST + ':' + PORT);
    // Write a message to the socket as soon as the client is connected, the server will receive it as message from the client

    client.write('Hello from Electron interface!\n#\n')
  });

  client.on('data', function(data) {

    test_relay.value += data;
    // Close the client socket completely
    client.destroy();
  });

  // Add a 'close' event handler for the client socket
  client.on('close', function() {
    console.log('Connection closed');
  });
});
