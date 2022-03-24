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