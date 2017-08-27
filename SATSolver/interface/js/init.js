const net = require('net');
var ProgressBar = require('progressbar.js');
const remote =  require('electron').remote;
const canvasBuffer = require('electron-canvas-to-buffer');

const {
  Menu,
  MenuItem
} = require('electron').remote;

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

var generations = new Vue({
    el: "#generations",
    data: {
      generations: 0,
      max_generations: 1000
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
    generations.generations = progressArray["GENERATION"][0];
    generations.max_generations = progressArray["GENERATION"][1];
    fitness.fitness = progressArray["BEST_INDIVIDUAL"][0];
    time_elapsed.started = progressArray["TIME_STARTED"][0]*1000;

    if (!chart.data.labels.includes(progressArray["GENERATION"][0])) {
      chart.data.labels.push(progressArray["GENERATION"][0]);
      chart.data.datasets[0].data.push(progressArray["BEST_INDIVIDUAL"][0]);
      chart.data.datasets[1].data.push(progressArray["CURRENT_CHILD_FITNESS"][0]);
      chart.update();
    }
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

var chart;
$(document).ready(function () {
    var accent_colour = $('button').css('backgroundColor');
    var ctx = document.getElementById('fitness-chart').getContext('2d');
    chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: [],
            datasets: [{
                label: "Fittest Individual",
                backgroundColor: accent_colour,
                borderColor: accent_colour,
                fill: false,
                lineTension: 0,
                data: []
            },{
                label: "Newest Child Fitness",
                backgroundColor: '#ccc',
                borderColor: '#ccc',
                fill: false,
                data: []
            }]
        },

        // Configuration options go here
        options: {
            elements: {
                line: {
                    tension: 0
                }
            },
            scales: {
                xAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: 'Generations'
                  },
                  ticks: {
                      autoSkip: true,
                      maxTicksLimit: 25
                  }
              }],
              yAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: 'Fitness (Unsolved Clauses)'
                  },
                  ticks: {
                      autoSkip: true,
                      maxTicksLimit: 25
                  }
              }]
            }
        }
    });
});

window.setInterval(function(){
  var calculated_elapsed = (((new Date).getTime() - time_elapsed.started));
  if (calculated_elapsed < 10000) {
    time_elapsed.elapsed = moment(calculated_elapsed).format('s') + 's';
  } else if (calculated_elapsed < 60000) {
    time_elapsed.elapsed = moment(calculated_elapsed).format('ss') + 's';
  } else if (calculated_elapsed < 600000) {
    time_elapsed.elapsed = moment(calculated_elapsed).format('m:ss');
  } else if (calculated_elapsed < 3600000) {
    time_elapsed.elapsed = moment(calculated_elapsed).format('mm:ss');
  } else if (calculated_elapsed < 36000000) {
    time_elapsed.elapsed = moment(calculated_elapsed-7200000).format('H:mm:ss');
  } else if (calculated_elapsed < 86400000) {
    time_elapsed.elapsed = moment(calculated_elapsed-7200000).format('HH:mm:ss');
  } else {
    time_elapsed.elapsed = moment(calculated_elapsed-93600000).format('DD:HH:mm:ss');
  }
}, 1000);
