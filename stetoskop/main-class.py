import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import librosa
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sn
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential, Model
from tensorflow.keras import regularizers, optimizers
from tensorflow.keras.layers import Dense, Conv1D, Flatten, Activation, MaxPooling1D, Dropout
from tensorflow.keras.utils import plot_model, to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# class diagnosa


class Diagnosis():
    def __init__(self, id, diagnosis, path):
        self.id = id
        self.diagnosis = diagnosis
        self.path = path

# get audio


def get_audio_files():
    audio_path = '/Users/mac/Downloads/ICBHI/'  # path database
    files = [f for f in listdir(audio_path) if isfile(
        join(audio_path, f))]  # all files
    audio_files = [f for f in files if f.endswith('.wav')]  # (.wav)
    audio_files = sorted(audio_files)
    return audio_files, audio_path

# diagnosa file


def diagnosis_data():
    diagnosis = pd.read_csv('/Users/mac/Downloads/ICBHI/diagnosis.txt')
    audio_files, audio_path = get_audio_files()
    diag_dict = {101: 'URTI'}  # dictionary w/ id and diagnosis
    diag_list = []

    for index, row in diagnosis.iterrows():
        i = row[0].split()
        diag_dict[int(i[0])] = i[1]

    # print(audio_files)

    i = 0
    for f in audio_files:
        idx = int(f[:3])
        # print(diag_dict[idx])
        diag = [i, diag_dict[idx], audio_path+f]
        # print(diag)
        diag_list.append(diag)
        i += 1
    return diag_list

# extract features


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
        sound, sr=sample_rate), axis=1)  # Mel-scaled spectrogram
    contrast = np.mean(librosa.feature.spectral_contrast(
        S=stft, sr=sample_rate), axis=1)  # Spectral contrast
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(
        sound), sr=sample_rate), axis=1)  # Tonal centroid features

    features = np.concatenate((mfccs, chroma, mel, contrast, tonnetz))
    return features

# data points


def data_points():
    labels = []
    images = []

    encoding = {"COPD": 0, "Healthy": 1, "URTI": 2, "Bronchiectasis": 3,
                "Pneumonia": 4, "Bronchiolitis": 5, "Asthma": 6, "LRTI": 7}

    i = 0
    for f in diagnosis_data():
        print(i)
        lbl = f[1]
        path = f[2]
        print(path)
        labels.append(encoding[lbl])  # copd
        images.append(audio_features(path))  # path
        i += 1
    return np.array(labels), np.array(images)

# pre processing


def preprocessing(labels, images):
    # Remove Asthma and LRTI because lack of data for those, will only hurt the model
    images = np.delete(images, np.where(
        (labels == 7) | (labels == 6))[0], axis=0)
    labels = np.delete(labels, np.where(
        (labels == 7) | (labels == 6))[0], axis=0)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        images, labels, test_size=0.2, random_state=10)

    # Hot one encode the labels
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    # Format new data
    y_train = np.reshape(y_train, (y_train.shape[0], 6))
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    y_test = np.reshape(y_test, (y_test.shape[0], 6))
    X_test = np.reshape(X_test, (X_test.shape[0], X_train.shape[1],  1))

    return X_train, X_test, y_train, y_test


# X, y = data_points()
# with open('features.npy', 'wb') as f:
#     np.save(f, X)
#     np.save(f, y)


def training(X, y):
    #print(X, y)
    print("Retrieving and processing data...")
    #labels, images = data_points()
    X_train, X_test, y_train, y_test = preprocessing(X, y)
    print("Finished data retrieval and preprocessing!")

    model = Sequential()
    model.add(Conv1D(64, kernel_size=5, activation='relu', input_shape=(193, 1)))

    model.add(Conv1D(128, kernel_size=5, activation='relu'))
    model.add(MaxPooling1D(2))

    model.add(Conv1D(256, kernel_size=5, activation='relu'))

    model.add(Dropout(0.3))
    model.add(Flatten())

    model.add(Dense(512, activation='relu'))
    model.add(Dense(6, activation='softmax'))

    checkpointer = ModelCheckpoint(filepath='digital_stetoskop.h5',
                                   verbose=1, save_best_only=True)
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])
    history = model.fit(X_train, y_train, validation_data=(
        X_test, y_test), epochs=100, batch_size=200, callbacks=[checkpointer], verbose=1)

    model.summary()
    score = model.evaluate(X_test, y_test, batch_size=60, verbose=0)
    print('Accuracy: {0:.2%}'.format(score[1]/1))
    print("Loss: %.4f\n" % score[0])
    print("---accuracy---")
    print(history.history['accuracy'])
    print(history.history['val_accuracy'])
    print("---loss---")
    print(history.history['loss'])
    print(history.history['val_loss'])


def chart_accuracy(history):
    # Plot accuracy and loss graphs
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    plt.title('Accuracy')
    plt.plot(history.history['accuracy'], label='training acc')
    plt.plot(history.history['val_accuracy'], label='validation acc')
    plt.legend()
    plt.show()


def chart_loss(history):
    plt.subplot(1, 2, 2)
    plt.title('Loss')
    plt.plot(history.history['loss'], label='training loss')
    plt.plot(history.history['val_loss'], label='validation loss')
    plt.legend()
    plt.show()


def confussion_matrix():
    matrix_index = ["COPD", "Healthy", "URTI",
                    "Bronchiectasis", "Pneumonia", "Bronchiolitis"]

    preds = model.predict(X_test)
    classpreds = np.argmax(preds, axis=1)  # predicted classes
    y_testclass = np.argmax(y_test, axis=1)  # true classes

    cm = confusion_matrix(y_testclass, classpreds)
    print(classification_report(y_testclass, classpreds, target_names=matrix_index))

    # Get percentage value for each element of the matrix
    cm_sum = np.sum(cm, axis=1, keepdims=True)
    cm_perc = cm / cm_sum.astype(float) * 100
    annot = np.empty_like(cm).astype(str)
    nrows, ncols = cm.shape
    for i in range(nrows):
        for j in range(ncols):
            c = cm[i, j]
            p = cm_perc[i, j]
            if i == j:
                s = cm_sum[i]
                annot[i, j] = '%.1f%%\n%d/%d' % (p, c, s)
            elif c == 0:
                annot[i, j] = ''
            else:
                annot[i, j] = '%.1f%%\n%d' % (p, c)

    # Display confusion matrix
    df_cm = pd.DataFrame(cm, index=matrix_index, columns=matrix_index)
    df_cm.index.name = 'Actual'
    df_cm.columns.name = 'Predicted'
    fig, ax = plt.subplots(figsize=(10, 7))
    sn.heatmap(df_cm, annot=annot, fmt='')
    plt.show()
# # 1. extract feature
# features = get_features()
# extracted_features = pd.DataFrame(features, columns=['feature', 'class'])
# # Split the dataset into independent and dependent dataset
# X = np.array(extracted_features['feature'].tolist())
# y = np.array(extracted_features['class'].tolist())

# load features
# print("Loadin features...")

# print("Train")
# # 2. train model
# train = get_train(X, y)


# 3. validate
# file = "/Users/mac/Downloads/Dataset/Pneumonia/226_1b1_Pl_sc_LittC2SE.wav"
# file = "/Users/mac/Downloads/Dataset/Healthy/184_1b1_Ar_sc_Meditron.wav"
# print(file)
# #file = os.curdir+'/'+'copd.wav'
# features = test_feature(file)
# get_validate(features)
with open('features.npy', 'rb') as f:
    X = np.load(f)
    y = np.load(f)
training(X, y)
