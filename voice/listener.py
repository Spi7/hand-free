import os
import wave
import tempfile
import threading
import audioop
import pyaudio
import re
from groq import Groq

RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 4
WAKE_WORD = "hello siri"
VOLUME_THRESHOLD = 400  

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def start_listening(on_command):

    def listen_loop():
        audio = pyaudio.PyAudio()
        print("Listening...")

        while True:
            # record audio from mic
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )

            frames = []
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            stream.stop_stream()
            stream.close()

            # check volume before sending to Groq
            raw_audio = b''.join(frames)
            rms = audioop.rms(raw_audio, 2)

            # save to temp wav file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_path = tmp.name

            with wave.open(tmp_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(RATE)
                wf.writeframes(raw_audio)

            try:
                if rms < VOLUME_THRESHOLD:
                    continue  # skip — too quiet, likely background noise

                with open(tmp_path, "rb") as audio_file:
                    transcription = client.audio.transcriptions.create(
                        model="whisper-large-v3",
                        file=audio_file,
                        language="en",
                        prompt="Hello Siri, exit, open, click, search"  # hint expected words
                    )

                text = re.sub(r'[^\w\s]', '', transcription.text).strip().lower()

                if not text:
                    continue

                print(f"Heard: {text} (volume: {rms})")

                if WAKE_WORD in text:
                    command = text.replace(WAKE_WORD, "").strip()
                    if command:
                        on_command(command)

            except Exception as e:
                print(f"Transcription error: {e}")

            finally:
                os.remove(tmp_path)

    thread = threading.Thread(target=listen_loop, daemon=True)
    thread.start()