from pydub import AudioSegment
import pyaudio
import wave


def start_recording(filename='sample'):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = 'sounds/'+filename+".wav"
    # MP3_OUTPUT_FILENAME = 'sounds/'+filename+".mp3"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Start recording "+filename+" for 5 seconds, please wait...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording "+filename+" done...")

    stream.stop_stream()
    stream.close()
    # p.terminate()

    print("Saving file "+WAVE_OUTPUT_FILENAME+" ...")
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("Done")
    # print("Converting wav to mp3 file...")

    # sound = AudioSegment.from_wav(WAVE_OUTPUT_FILENAME)

    # sound.export(MP3_OUTPUT_FILENAME, format='mp3')

    # print("Done... ")
