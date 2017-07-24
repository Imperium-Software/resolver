let net = require('net');
let fs = require('fs');
const {
    dialog
} = require('electron').remote;

let HOST = 'rainmaker.wunderground.com';
let PORT = 23;

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
    menuWidth: 300, // Default is 300
    edge: 'left', // Choose the horizontal origin
    closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor
    draggable: true, // Choose whether you can drag to open on touch screens,
    //onOpen: function(el) { /* Do Stuff* / }, // A function to be called when sideNav is opened
    //onClose: function(el) { /* Do Stuff* / }, // A function to be called when sideNav is closed
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

        app = new Vue({
            el: '#perc',
            data: {
                percentage: app.percentage
            }
        })
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
            break;

    }
}