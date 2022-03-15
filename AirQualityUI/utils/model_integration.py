import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras.models import load_model


weather_event_cat = {
    'inconnu': 1, 'pluie faible': 2, 'ciel clair': 3, 'brouillard faible': 4, 'pluie': 5, 'brouillard': 6,
    'neige faible': 7, 'pluie forte': 8, 'neige': 9, 'brouillard fort': 10
}

atmo_cat = {'bon': 1, 'moyen': 2, 'dégradé': 3, 'mauvais': 4, "très mauvais": 5, "extrêmement mauvais": 6}

wind_dir_cat = {
    'SO': 1, 'O': 2, 'SSO': 3, 'N': 4, 'S': 5, 'NE': 6, 'OSO': 7, 'NNO': 8, 'ONO': 9, 'ENE': 10, 'E': 11,
    'NNE': 12, 'NO': 13, 'SSE': 14, 'SE': 15, 'ESE': 16
}


def formatDataframe(df):
    data = df.copy().drop("date", axis=1)
    data["wind_dir_cat"] = data.wind_dir.apply(lambda x: wind_dir_cat[x])
    data["weather_event_cat"] = data.weather_event.apply(lambda x: weather_event_cat[x])
    data["atmo_cat"] = data.ATMO.apply(lambda x: atmo_cat[x])
    data = data.drop(["ATMO", "weather_event", "wind_dir"], axis=1)
    return data


def getPredictions(modelPath, X_predict):
    model = load_model(modelPath)
    y_pred = model.predict(X_predict)
    return y_pred
