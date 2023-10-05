import wave
import sys
import pyaudio
from pydub import AudioSegment
from settings import *

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 30

INPUT_FILE_NAME = "input.wav"
OUTPUT_FILE_NAME = "output.mp3"

def record(second: int, mc_id: int) -> str:
    file = MEDIA_PATH + INPUT_FILE_NAME
    wf = wave.open(file, 'wb')
    audio = pyaudio.PyAudio()
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=mc_id)

    print('Recording...')
    for _ in range(0, RATE // CHUNK * second):
        wf.writeframes(stream.read(CHUNK))
    print('Done')

    stream.close()
    audio.terminate()
    wf.close()

    file = converter_from_wav_to_mp3(file)

    return file

def choose_microphone() -> None:
    audio = pyaudio.PyAudio()
    for i in range(audio.get_device_count()):
        print(i, audio.get_device_info_by_index(i)['name'])

def converter_from_wav_to_mp3(audio_file: str) -> str:
    file = MEDIA_PATH + OUTPUT_FILE_NAME
    sound = AudioSegment.from_wav(audio_file)
    sound.export(file, format="mp3")

    return OUTPUT_FILE_NAME
