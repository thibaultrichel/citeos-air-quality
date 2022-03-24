const tf = require("@tensorflow/tfjs");
const csv = require("jquery-csv");

async function loadModel() {
    return await tf.loadLayersModel("/Users/thibaultrichel/Desktop/JupyterLab/ProjetCITEOS/WebUI/model_utils/tfjsmodel/model.json");
}

let model = loadModel();
// let data = csv.toObjects("model_utils/merged-final.csv");
// let size = data.size;
//
// module.exports = {size};
//
// console.log(size);

console.log(model);
