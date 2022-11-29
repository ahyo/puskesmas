import json
from keras.models import load_model
from classification import audio_features
import numpy as np


def validate_file(file):
    labels = ["COPD", "Healthy", "URTI",
              "Bronchiectasis", "Pneumonia", "Bronchiolitis"]

    #file = "/Users/mac/Downloads/ICBHI/111_1b2_Tc_sc_Meditron.wav"
    features = audio_features(file)
    X = features.reshape(1, -1)

    model = load_model("digital_stetoskop.h5")
    predictions = model.predict(X)
    pred = np.argmax(predictions)
    return labels[pred]
