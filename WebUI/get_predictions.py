import json
from tensorflow.keras.models import load_model


def loadModel():
    path = "model_utils/LSTM_multi_with_target.h5"
    return load_model(path)


def getPredictions(data):
    model = loadModel()
    y_pred = model.predict(data)
    val = y_pred[0][0]
    output = {
        "result": val
    }
    return json.dumps(output)
