var mathjaxHelper = require('mathjax-electron')
var cnf = document.getElementById('cnf-example')
cnf.innerHTML = '$$(a \\vee b \\vee c ) \\wedge (b \\vee d)$$'
mathjaxHelper.typesetMath(cnf)