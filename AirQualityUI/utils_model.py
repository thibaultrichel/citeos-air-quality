from keras.models import load_model


def getModel(path):
    model = load_model(path)
    model.summary()


modelPath = ""
getModel(modelPath)
