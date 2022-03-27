import json
import numpy as np
import pandas as pd
from keras.models import load_model
import os



def loadModel():
    path = "./models/LSTM_multi_with_target.h5"
    return load_model(path)


def getPredictions(data):
    model = loadModel()
    y_pred = model.predict(data)
    return {"result": str(y_pred[0][0])}


weather_event_cat = {
    'inconnu': 1, 'pluie faible': 2, 'ciel clair': 3, 'brouillard faible': 4, 'pluie': 5, 'brouillard': 6,
    'neige faible': 7, 'pluie forte': 8, 'neige': 9, 'brouillard fort': 10
}

atmo_cat = {'bon': 1, 'moyen': 2, 'dégradé': 3, 'mauvais': 4, "très mauvais": 5, "extrêmement mauvais": 6}

wind_dir_cat = {
    'SO': 1, 'O': 2, 'SSO': 3, 'N': 4, 'S': 5, 'NE': 6, 'OSO': 7, 'NNO': 8, 'ONO': 9, 'ENE': 10, 'E': 11,
    'NNE': 12, 'NO': 13, 'SSE': 14, 'SE': 15, 'ESE': 16
}

df = pd.read_csv("https://raw.githubusercontent.com/thibaultrichel/citeos-air-quality/main/data/final/merged-final.csv",
                 sep=';').dropna().drop("day", axis=1)
df["wind_dir_cat"] = df.wind_dir.apply(lambda x: wind_dir_cat[x])
df["weather_event_cat"] = df.weather_event.apply(lambda x: weather_event_cat[x])
df["atmo_cat"] = df.ATMO.apply(lambda x: atmo_cat[x])
df = df.drop(["ATMO", "weather_event", "wind_dir"], axis=1)
values = df.drop("date", axis=1).values
train_size = int(values.shape[0] * 0.75)
n_past = 120
n_future = 12
X_val = np.array(values[train_size:train_size + n_past])
X_val = np.expand_dims(X_val, axis=0)

output = getPredictions(X_val)
print(output)

with open("./result.json", "w") as file:
    file.write(json.dumps(output, indent=4))
file.close()
