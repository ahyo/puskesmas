from keras.models import load_model
import numpy as np
import librosa
import argparse
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def audio_features(filename):
    sound, sample_rate = librosa.load(filename)
    # short-time Fourier transform (STFT) spectrogram
    stft = np.abs(librosa.stft(sound))

    # Mel-frequency cepstral coefficients
    mfccs = np.mean(librosa.feature.mfcc(
        y=sound, sr=sample_rate, n_mfcc=40), axis=1)
    # Chromagram from STFT spectrogram
    chroma = np.mean(librosa.feature.chroma_stft(
        S=stft, sr=sample_rate), axis=1)
    mel = np.mean(librosa.feature.melspectrogram(
        y=sound, sr=sample_rate), axis=1)  # Mel-scaled spectrogram
    contrast = np.mean(librosa.feature.spectral_contrast(
        S=stft, sr=sample_rate), axis=1)  # Spectral contrast
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(
        y=sound), sr=sample_rate), axis=1)  # Tonal centroid features

    features = np.concatenate((mfccs, chroma, mel, contrast, tonnetz))
    return features


def validate_file(file):
    labels = ["COPD", "Healthy", "URTI",
              "Bronchiectasis", "Pneumonia", "Bronchiolitis"]

    #file = "/Users/mac/Downloads/ICBHI/111_1b2_Tc_sc_Meditron.wav"
    features = audio_features(file)
    X = features.reshape(1, -1)

    model = load_model(os.getcwd()+"/digital_stetoskop.h5")
    predictions = model.predict(X)
    pred = np.argmax(predictions)
    return labels[pred]


# if __name__ == "__main__":

#     parser = argparse.ArgumentParser(description="Klasifikasi file respiratory",
#                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#     parser.add_argument("-f", "--file", help="file yang akan diproses")
#     args = parser.parse_args()
#     file = vars(args)['file']
#     if not file:
#         print("---Harap mencantumkan nama file")
#         exit()
#     if not os.path.isfile(file):
#         print("---File "+file+" tidak valid")
#         exit()
#     result = validate_file(file)
#     print("---"+result)
