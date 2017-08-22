const net = require('net');

// Bindings

var perc = new Vue({
  el: '#perc',
  data: {
    percentage: 0
  }
});

var terminal = new Vue({
	el: '#term',
	data : {
		text : ""
	}
});

var error_log = new Vue({
  el: "#err",
  data : {
    text : ""
  }
});

connected = "red";

// Connection

// Create connection and establish callbacks.

conn = new net.Socket();

conn.connect(process.env.SAT_SOLVER_PORT, '127.0.0.1', function() {
    console.log('Connected');
    $("#connected-indicator")[0].style.fill = lime;
    connected = "lime;"
});

conn.on('data', function(data) {
  console.log('Received: ' + data);
  terminal.text += "\n" + data;
});
conn.on('close', function() {
  console.log('Connection closed');
  $("#connected-indicator")[0].style.fill = "red";
  connected = "red";
});