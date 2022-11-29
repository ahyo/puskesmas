import matplotlib.pyplot as plt
import librosa.display

import numpy as np
import pandas as pd
import librosa


def generate_image(filename='sample'):
    file = 'images/'+filename+'.png'
    print("generate image "+file)
    #filename = librosa.util.example_audio_file()
    y, sr = librosa.load('sounds/'+filename+'.wav')
    y = y[:100000]  # shorten audio a bit for speed

    window_size = 1024
    window = np.hanning(window_size)
    stft = librosa.core.spectrum.stft(
        y, n_fft=window_size, hop_length=512, window=window)
    out = 2 * np.abs(stft) / np.sum(window)

    # For plotting headlessly
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

    fig = plt.Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    p = librosa.display.specshow(librosa.amplitude_to_db(
        out, ref=np.max), ax=ax, y_axis='log', x_axis='time')
    fig.savefig(file)
    print("Done")


def generate_spectogram(source='source.wav', target='target.png'):
    print('loading '+source)
    #filename = librosa.util.example_audio_file()
    y, sr = librosa.load(source)
    y = y[:100000]  # shorten audio a bit for speed

    window_size = 1024
    window = np.hanning(window_size)
    stft = librosa.core.spectrum.stft(
        y, n_fft=window_size, hop_length=512, window=window)
    out = 2 * np.abs(stft) / np.sum(window)

    # For plotting headlessly
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

    fig = plt.Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    p = librosa.display.specshow(librosa.amplitude_to_db(
        out, ref=np.max), ax=ax, y_axis='log', x_axis='time')
    fig.savefig(target)
    print('generated '+target)
