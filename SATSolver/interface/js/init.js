const net = require('net');
var ProgressBar = require('progressbar.js');

var progress_bar = new ProgressBar.Circle('#progress-circle', {
  color: '#FFF',
  // This has to be the same size as the maximum width to
  // prevent clipping
  strokeWidth: 10,
  trailWidth: 3,
  easing: 'easeInOut',
  duration: 1400,
  text: {
    autoStyleContainer: true
  },
  from: { color: '#aaa', width: 4 },
  to: { color: '#333', width: 4 },
  // Set default step function for all animate calls
  step: function(state, circle) {
    circle.path.setAttribute('stroke', state.color);
    circle.path.setAttribute('stroke-width', state.width);
    var value = Math.round(circle.value() * 1000) / 10;

    if (value === 0) {
      circle.setText('0');
    } else {
      circle.setText(value);
    }

  }
});

progress_bar.animate(0.0);

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

conn.connect(55555, '127.0.0.1', function() {
    console.log('Connected');
    $("#connected-indicator")[0].style.fill = "lime";
    connected = "lime"
});

conn.on('data', function(data) {
  data = data.slice(0, -1);
  console.log('Received: ' + data);
  terminal.text += "\n" + data;
  progressObject = JSON.parse(data);
  progressArray = progressObject["RESPONSE"]["PROGRESS"]["GENERATION"];
  perc.percentage = progressArray[0] / progressArray[1];
  progress_bar.animate(progressArray[0] / progressArray[1]);
});
conn.on('close', function() {
  console.log('Connection closed');
  $("#connected-indicator")[0].style.fill = "red";
  connected = "red";
});