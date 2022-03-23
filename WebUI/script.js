// const csv = require("jquery-csv");
// let data = csv.toObjects("model_utils/merged-final.csv");

const getValue = () => {
    return 3.4
}

const displayPred = () => {
    const base = "Prediction result : ";
    document.getElementById("pred-result").innerHTML = base + "<b>" + getValue() + "</b>";
};
