import os
from PyQt5.QtGui import QPixmap
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

label_positions = {i+1: (40 + i * 75, 130) for i in range(6)}
advices = {
    1: "Bonne qualité de l'air :)",
    2: "Qualité de l'air moyenne, privilégiez les transports",
    3: "Qualité de l'air dégradé, évitez de prendre votre voiture",
    4: "Mauvaise qualité de l'air, ne prenez pas votre voiture",
    5: "Très mauvaise qualité de l'air, attention pour votre santé",
    6: "Qualité de l'air excrécrable, mettez un masque"
}


def getColorAndIcon(value):
    color = ""
    if 0 < value <= 1:
        color = "cyan"
    elif 1 < value <= 2:
        color = "lime"
    elif 2 < value <= 3:
        color = "yellow"
    elif 3 < value <= 4:
        color = "orange"
    elif 4 < value <= 5:
        color = "red"
    elif value > 5:
        color = "purple"
    return color


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
