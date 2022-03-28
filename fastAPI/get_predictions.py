import numpy as np
import pandas as pd
from keras.models import load_model


def loadModel():
    path = "../models/LSTM_multi_with_target.h5"
    return load_model(path)


def loadDataset():
    return pd.read_csv("https://raw.githubusercontent.com/thibaultrichel/citeos-air-quality/main/data/final/merged"
                       "-cleaned-final.csv", sep=';')


def getPredictions():
    df = loadDataset()
    values = df.drop("date", axis=1).values
    train_size = int(values.shape[0] * 0.75)
    n_past = 120
    X_val = np.array(values[train_size:train_size + n_past])
    X_val = np.expand_dims(X_val, axis=0)
    model = loadModel()
    y_pred = model.predict(X_val)
    return str(y_pred[0][0])
