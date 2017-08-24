const net = require('net');
var ProgressBar = require('progressbar.js');

var progress_bar = new ProgressBar.Circle('#progress-circle', {
  color: '#FFF',
  strokeWidth: 15,
  trailWidth: 4,
  easing: 'easeInOut',
  duration: 1400,
  text: {
    autoStyleContainer: true
  },
  from: { color: '#0EBFE9', width: 4 },
  to: { color: '#0EBFE9', width: 4 },
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

var time_elapsed = new Vue({
   el: "#time",
    data: {
     elapsed: 0,
        started: 0
    }
});

var fitness = new Vue({
    el: "#fitness",
    data: {
      fitness: 0
    }
});

connected = false;

// Connection

// Create connection and establish callbacks.

conn = new net.Socket();

conn.connect(55555, '127.0.0.1', function() {
    console.log('Connected');
    $("#connected-indicator")[0].style.fill = "lime";
    connected = true;
});

conn.on('data', function(data) {
  data = data.slice(0, -1);
  console.log('Received: ' + data);
  terminal.text += "\n" + data;
  try {
    progressObject = JSON.parse(data);
    progressArray = progressObject["RESPONSE"]["PROGRESS"];
    perc.percentage = progressArray["GENERATION"][0] / progressArray["GENERATION"][1];
    perc.percentage = progressArray["GENERATION"][0] / progressArray["GENERATION"][1];
    fitness.fitness = progressArray["BEST_INDIVIDUAL"][0];
    time_elapsed.started = progressArray["TIME_STARTED"][0]*1000;
  } catch(e) {
    $("#connected-indicator")[0].style.fill = "yellow";
    //alert("WTF man, wat even is this.")
      console.log(e)
  }
  progress_bar.animate(perc.percentage);
});

conn.on('close', function() {
  console.log('Connection closed');
  $("#connected-indicator")[0].style.fill = "red";
  connected = false;
});

window.setInterval(function(){
  time_elapsed.elapsed = moment(((new Date).getTime() - time_elapsed.started)-7200000).format('HH:mm:ss');
}, 1000);