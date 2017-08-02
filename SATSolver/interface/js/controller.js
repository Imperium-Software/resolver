let net = require('net');
let fs = require('fs');
const { dialog } = require('electron').remote;

let HOST = 'localhost';
let PORT = 23;

function construct_request() {
    var request_string = "";

    // Add terminating character.
    return request_string.concat('#')
}

//select drowpdowns
$(document).ready(function() {
    $('select').material_select();
});

//open file
// document.getElementById('open-file').addEventListener('click', () => {
//   dialog.showOpenDialog((filename) => {
//     if (filename === undefined) {
//       console.log('The user did not select a location to open.')
//       return
//     }
//     console.log(filename)
//     fs.readFile(filename[0], 'utf8', (err, data) => {
//       if (err) {
//         console.log(err)
//         return
//       }
//       editor.value = data;
//       toggle_hex = false;
//     })
//   })
// })

// document.getElementById('open-file').addEventListener("click", () => {

//   if(true)
//   {
//     dialog.showOpenDialog((filename) => {
//     if (filename === undefined) {
//       console.log('The user did not select a location to open.')
//       return
//     }
//     console.log(filename)
//     fs.readFile(filename[0], 'utf8', (err, data) => {
//       if (err) {
//         console.log(err)
//         return
//       }
//       editor.value = data;
//       toggle_hex = false;
//     })
//   })
//   } 

// })

// document.getElementById('open-file2').addEventListener("change", () => {

//   if(this.options[this.selctedIndex].value == "1")
//   {
//     dialog.showOpenDialog((filename) => {
//     if (filename === undefined) {
//       console.log('The user did not select a location to open.')
//       return
//     }
//     console.log(filename)
//     fs.readFile(filename[0], 'utf8', (err, data) => {
//       if (err) {
//         console.log(err)
//         return
//       }
//       editor.value = data;
//       toggle_hex = false;
//     })
//   })
//   } 

// })

// Side Nav

$(".button-collapse").sideNav();

$('.button-collapse').sideNav({
    menuWidth: 300,
    edge: 'left',
    closeOnClick: true,
    draggable: true,
});

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
        render();

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
                text : terminal.text
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
            document.body.style.setProperty("--theme-background","#f0f3f4");
            break;
        case "halloween":
            document.body.style.setProperty("--theme-one", "#121415");
            document.body.style.setProperty("--theme-two", "#FD971F");
            document.body.style.setProperty("--theme-three", "#283137");
            document.body.style.setProperty("--theme-four", "#F37259");
            document.body.style.setProperty("--theme-five", "#66D9EF");
            document.body.style.setProperty("--theme-background","#f0f3f4");
            break;
        case "iphone":
            document.body.style.setProperty("--theme-one", "black");
            document.body.style.setProperty("--theme-two", "black");
            document.body.style.setProperty("--theme-three", "black");
            document.body.style.setProperty("--theme-four", "#222");
            document.body.style.setProperty("--theme-five", "black");
            document.body.style.setProperty("--theme-background","#586e75");
            break;
    }

    fs.writeFile("css/current-theme-init.css", 
        ":root {" +
        "--theme-one:"   + document.body.style.getPropertyValue('--theme-one') + ";\n" + 
        "--theme-two:"   + document.body.style.getPropertyValue('--theme-two') + ";\n" +
        "--theme-three:" + document.body.style.getPropertyValue('--theme-three') + ";\n" +
        "--theme-four:"  + document.body.style.getPropertyValue('--theme-four') + ";\n" +
        "--theme-five:"  + document.body.style.getPropertyValue('--theme-five') + ";\n" +
        "--theme-background:"  + document.body.style.getPropertyValue('--theme-background') + ";\n" +
        "}"
        , 
        function(err) {
    if(err) {
        return console.log(err);
    }}); 
}

function make_request() {
    alert('hi!')
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