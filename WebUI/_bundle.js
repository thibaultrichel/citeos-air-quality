(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
// const module = require("./module.js");

module.displayPred();
},{"./module.js":2}],2:[function(require,module,exports){
const spawner = require("child_process").spawn;

const getValue = () => {
    let output = {}
    const pyprocess = spawner("python", ["./get_predictions"]);
    pyprocess.stdout.on("data", (data) => {
        output = JSON.parse(data.toString());
        console.log(output);
    });
    return output;
}

const displayPred = () => {
    const base = "Prediction result : ";
    const val = getValue()["result"];
    document.getElementById("pred-result").innerHTML = base + "<b>" + val + "</b>";
};

module.exports = {displayPred: displayPred};
},{"child_process":3}],3:[function(require,module,exports){

},{}]},{},[1]);
