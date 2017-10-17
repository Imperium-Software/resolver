var fs = require('fs');
const {
    dialog
} = require('electron').remote;

function construct_request(type) {
    var request_string = '';
    if (type === 'SOLVE') {

        var dimacs;

        if ($('#cnf-input-method')[0].value === 'file') {
            var filename = $('#selected-file').prop('files')[0].path;
            dimacs = fs.readFileSync(filename).toString().trim()
        } else {
            dimacs = $('#manual-cnf')[0].value;
        }

        var max_generations_input = $('#max_generations')[0].value;
        var population_size_input = $('#population_size')[0].value;
        var sub_population_size_input = $('#sub_population_size')[0].value;
        var max_flip_input = $('#max_flip')[0].value;
        var crossover_operator_input = $('#crossover_operator')[0].value;
        var method_input = $('#method')[0].value;
        var tabu_settings_input = $('#tabu-settings').val();

        var request = {
            "SOLVE": {
                "raw_input": null,
                "tabu_list_length": null,
                "max_false": null,
                "rec": null,
                "k": null
            }
        };

        request.SOLVE.tabu_list_length = $("#tabu_list_length")[0].value;
        request.SOLVE.max_false = $("#max_false")[0].value;
        request.SOLVE.rec = $("#rec")[0].value;
        request.SOLVE.k = $("#k")[0].value;

        if (population_size_input !== undefined && population_size_input !== '') {
            request.SOLVE["population_size"] = population_size_input;
        }

        if (sub_population_size_input !== undefined && sub_population_size_input !== '') {
            request.SOLVE["sub_population_size"] = parseInt(sub_population_size_input);
        }

        if (crossover_operator_input !== undefined && crossover_operator_input !== '') {
            request.SOLVE["crossover_operator"] = parseInt(crossover_operator_input);
        }

        if (max_flip_input !== undefined && max_flip_input !== '') {
            request.SOLVE["max_flip"] = parseInt(max_flip_input);
        }

        if (max_generations_input !== undefined && max_generations_input !== '') {
            request.SOLVE["max_generations"] = parseInt(max_generations_input);
        }

        if (method_input !== undefined && method_input !== '') {
            request.SOLVE["method"] = parseInt(method_input);
        }

        if (tabu_settings_input.indexOf('rvcf') !== -1) {
            request.SOLVE["is_rvcf"] = true;
        }

        if (tabu_settings_input.indexOf('diversification') !== -1) {
            request.SOLVE["is_diversification"] = true;
        }

        request.SOLVE.raw_input = dimacs.split('\n');
        for (var i = request.SOLVE.raw_input.length-1; i>=0; i--) {
            if (request.SOLVE.raw_input[i][0] === 'c') {
                request.SOLVE.raw_input.splice(i, 1);
            }
        }
        request_string = JSON.stringify(request);
    } else if (type === 'POLL') {
        request_string += "'POLL'";
    } else if (type === 'STOP') {
        request = {
            "STOP": {}
        };
        request_string = JSON.stringify(request);
    }
    // Add terminating character.
    return request_string + '#';
}

function make_request(type) {
    try {
        var request;
        if (type === 'SOLVE') {
            request = construct_request('SOLVE');
            console.log(request);
            conn.write(request);
            terminal.text = "";
            error_log.text = "";
        } else if (type === 'STOP') {
            request = construct_request('STOP');
            console.log(request);
            conn.write(request);
        }
    } catch (e) {
        console.log(e);
    }
    circularHeatChart([[1,0,1,0,1,1,0,1,0]], 10);
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
    console.log(process.resourcesPath + '/app/' + filename);
    // filename = process.resourcesPath + '/app/' + filename;
    fs.readFile(filename, 'utf8', (err, data) => {
        document.getElementById('base').innerHTML = data;
        document.body.classList.add('loaded');
        $(".button-collapse").sideNav();
        $('select').material_select();
        $('.collapsible').collapsible({
            accordion: true
        });
        $("#advanced").modal();
        $("#connected-indicator")[0].style.fill = conn.connected ? "lime" : "red";

        if (generations.generations == 0) {
            $("#progress").hide();
        }

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
            from: {
                color: '#0EBFE9',
                width: 4
            },
            to: {
                color: '#0EBFE9',
                width: 4
            },
            step: function (state, circle) {
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

        best_individual = new Vue({
            el: "#fitness",
            data: {
              fitness: best_individual.fitness,
              individual: best_individual.individual
            }
        });

        current_child = new Vue({
            data: {
              fitness: current_child.fitness,
              individual: current_child.individual,
              array : current_child.array

            }
        });

        formula_info = new Vue({
            el: "#formula-info",
            data: {
                num_clauses: formula_info.num_clauses,
                num_variables: formula_info.num_variables
            }
        });

        generations = new Vue({
            el: "#generations",
            data: {
                generations: generations.generations,
                max_generations: generations.max_generations
            }
        });

    })
    reset();
}

function theme_change() {
    var theme_select = document.getElementById('theme-select');
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
    var select_box = document.getElementById('cnf-input-method');
    if (select_box.value === "file") {
        $('#input-cnf-file').attr('hidden', false);
        $('#input-cnf-text').attr('hidden', true);
    } else {
        $('#input-cnf-file').attr('hidden', true);
        $('#input-cnf-text').attr('hidden', false);
    }
}

var fitness_chart = $("#fitness-chart")[0];
var menu = new Menu();
menu.append(new MenuItem({
    label: 'Save Graph To JPG',
    click: function (e) {
        dialog.showSaveDialog(function (fileName) {
            if (fileName !== undefined) {
                destinationCanvas = document.createElement("canvas");
                destinationCanvas.width = fitness_chart.width;
                destinationCanvas.height = fitness_chart.height;
                destCtx = destinationCanvas.getContext('2d');
                //create a rectangle with the desired color
                destCtx.fillStyle = "#FFFFFF";
                destCtx.fillRect(0,0,fitness_chart.width,fitness_chart.height);
                //draw the original canvas onto the destination canvas
                destCtx.drawImage(fitness_chart, 0, 0);
                var buffer = canvasBuffer(destinationCanvas, 'image/jpg')
                fs.writeFile(fileName, buffer, function (err) {
                    if (err) {
                        console.log(err);
                    }
                })
            }
        });
    }
}));

menu.append(new MenuItem({
    label: 'Save Graph To CSV',
    click: function (e) {
        dialog.showSaveDialog(function (fileName) {
            if (fileName !== undefined) {
                fs.writeFile(fileName + ".best.csv", chart.data["datasets"][0].data, function (err) {
                    console.log(err);
                });
                fs.writeFile(fileName + ".child.csv", chart.data["datasets"][1].data, function (err) {
                    console.log(err);
                });
            }
        });
    }
}));

fitness_chart.addEventListener('contextmenu', function (e) {
    e.preventDefault();
    menu.popup(remote.getCurrentWindow());
}, false);



