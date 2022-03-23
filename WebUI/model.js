const tf = require("@tensorflow/tfjs");
const csv = require("jquery-csv");

const model = await tf.loadLayersModel("model_utils/LSTM_multi_with_target.h5");
let data = csv.toObjects("model_utils/merged-final.csv");
let size = data.size;

module.exports = {size};