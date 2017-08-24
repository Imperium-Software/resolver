let fs = require('fs');
const {
    dialog
} = require('electron').remote;

function construct_request(type) {
    var request_string = '{ "command" :';
    var request_string = '';
    if (type == 'SOLVE') {

        var request_string = '{ "SOLVE" : {';

        if ($('#cnf-input-method')[0].value == 'file') {
            let filename = $('#selected-file').prop('files')[0].path;
            dimacs = fs.readFileSync(filename).toString().trim()
        } else {
            dimacs = $('#manual-cnf')[0].value;
        }

        // Mandatory parameters

        request_string += '"tabu_list_length" : ' + $("#tabu_list_length")[0].value;
        request_string += ',"max_false" : ' + $("#max_false")[0].value;
        request_string += ',"rec" : ' + $("#rec")[0].value;
        request_string += ',"k" : ' + $("#k")[0].value;

        // Optional parameters

        // Get optional inputs

        let max_generations_input = $('#max_generations')[0].value;
        let population_size_input = $('#population_size')[0].value;
        let sub_population_size_input = $('#sub_population_size')[0].value;
        let max_flip_input = $('#max_flip')[0].method;
        let crossover_operator_input = $('#crossover_operator')[0].value;
        let method_input = $('#method')[0].value;
        let tabu_settings_input = $('#tabu-settings').val();

        if (population_size_input != undefined && population_size_input != '') {
            request_string += ',"population_size" : ' + population_size_input;
        }

        if (sub_population_size_input != undefined && sub_population_size_input != '') {
            request_string += ',"sub_population_size" : ' + sub_population_size_input;
        }

        if (crossover_operator_input != undefined && crossover_operator_input != '') {
            request_string += ',"crossover_operator" : ' + crossover_operator_input;
        }

        if (max_flip_input != undefined && max_flip_input != '') {
            request_string += ',"max_flip" : ' + max_flip_input;
        }

        if (max_generations_input != undefined && max_generations_input != '') {
            request_string += ',"max_generations" : ' + max_generations_input;
        }

        if (method_input != undefined && method_input != '') {
            request_string += ',"method" : "' + method_input + '"';
        }

        if (tabu_settings_input.indexOf('rvcf') != -1) {
            request_string += ',"is_rvcf" : true';
        }
        
        if (tabu_settings_input.indexOf('diversification') != -1) {
            request_string += ',"is_diversification" : true';
        }

        request_string += ',"raw_input" : [ "' + dimacs.split('\n').join('","') + '"]';
        request_string = request_string.replace(/(\r\n|\n|\r)/gm,"");
    } else if (type == 'POLL') {
        request_string += "'POLL'";
    }
    // Add terminating character.
    return request_string + '}}#' ;
    // return '{ "SOLVE" : {"tabu_list_length" : 10,"max_false" : 5,"rec" : 5,"k" : 5,"raw_input" : [ "c FILE: trivial.cnf","c","c DESCRIPTION: Small expression used for testing purposes.","c","c NOTE: Satisfiable by design","c","p cnf 9 5","9 -5 0","1 3 6 0","2 -4 6 0","7 8 -3 0","-6 -4 0"]}}#'
}

function make_request(type, filename) {
    try {
        var request = construct_request('SOLVE');
        console.log(request);
        conn.write(request);
        terminal.text = "";
        error_log.text = "";
    } catch (e) {
        console.log(e);
    }
}

//select drowpdowns
$(document).ready(function () {
    $('select').material_select();
});

// Side Nav

$(".button-collapse").sideNav();

$('.button-collapse').sideNav({
    menuWidth: 300,
    edge: 'left',
    closeOnClick: true,
    draggable: true,
});

$("#advanced").modal();

// Progress Circle

$('#circle').circleProgress({
    value: 0.75,
    size: 40,
    fill: {
        gradient: ["lightblue", "grey"]
    }
});

function navigate(filename) {
    fs.readFile(filename, 'utf8', (err, data) => {
        document.getElementById('base').innerHTML = data;
        document.body.classList.add('loaded')
        $(".button-collapse").sideNav();
        $('select').material_select();
        $('.collapsible').collapsible({
            accordion: true
        });
        $("#advanced").modal();
        $("#connected-indicator")[0].style.fill = connected ? "lime" : "red";
        
        // Progress circle

        var new_progress_bar = new ProgressBar.Circle('#progress-circle', {
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
          
        //new_progress_bar.animate(progress_bar)
        new_progress_bar.animate(perc.percentage);
        progress_bar = new_progress_bar;


        // Re-render percentage

        perc = new Vue({
            el: '#perc',
            data: {
                percentage: perc.percentage
            }
        });

        terminal = new Vue({
            el: '#term',
            data: {
                text: terminal.text
            }
        });

        error_log = new Vue({
            el: '#err',
            data: {
                text: error_log.text
            }
        });

        time_elapsed = new Vue({
           el: "#time",
            data: {
             elapsed: time_elapsed.elapsed
            }
        });

        var fitness = new Vue({
            el: "#fitness",
            data: {
              fitness: 0
            }
        });

    })
}

function theme_change() {
    let theme_select = document.getElementById('theme-select');
    switch (theme_select.value) {
        case "tea":
            document.body.style.setProperty("--theme-one", "#364958");
            document.body.style.setProperty("--theme-two", "#3B6064");
            document.body.style.setProperty("--theme-three", "#3B6064");
            document.body.style.setProperty("--theme-four", "#ADC698");
            document.body.style.setProperty("--theme-five", "#C9E4CA");
            document.body.style.setProperty("--theme-background", "#f0f3f4");
            break;
        case "halloween":
            document.body.style.setProperty("--theme-one", "#121415");
            document.body.style.setProperty("--theme-two", "#FD971F");
            document.body.style.setProperty("--theme-three", "#283137");
            document.body.style.setProperty("--theme-four", "#F37259");
            document.body.style.setProperty("--theme-five", "#66D9EF");
            document.body.style.setProperty("--theme-background", "#f0f3f4");
            break;
        case "iphone":
            document.body.style.setProperty("--theme-one", "black");
            document.body.style.setProperty("--theme-two", "black");
            document.body.style.setProperty("--theme-three", "black");
            document.body.style.setProperty("--theme-four", "#222");
            document.body.style.setProperty("--theme-five", "black");
            document.body.style.setProperty("--theme-background", "#586e75");
            break;
    }

    fs.writeFile("css/current-theme-init.css",
        ":root {" +
        "--theme-one:" + document.body.style.getPropertyValue('--theme-one') + ";\n" +
        "--theme-two:" + document.body.style.getPropertyValue('--theme-two') + ";\n" +
        "--theme-three:" + document.body.style.getPropertyValue('--theme-three') + ";\n" +
        "--theme-four:" + document.body.style.getPropertyValue('--theme-four') + ";\n" +
        "--theme-five:" + document.body.style.getPropertyValue('--theme-five') + ";\n" +
        "--theme-background:" + document.body.style.getPropertyValue('--theme-background') + ";\n" +
        "}",
        function (err) {
            if (err) {
                return console.log(err);
            }
        });
}

function input_method_change() {
    let select_box = document.getElementById('cnf-input-method');
    if (select_box.value == "file") {
        $('#input-cnf-file').attr('hidden', false);
        $('#input-cnf-text').attr('hidden', true);
    } else {
        $('#input-cnf-file').attr('hidden', true);
        $('#input-cnf-text').attr('hidden', false);
    }
}