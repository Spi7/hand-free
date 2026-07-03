import speech_recognition as sr
import threading

def start_listening(on_command):
    # on_command would be a callback func - when a command is head
    # we call on_command(text) to pass the result back to main.py

    def listen_loop():
        wake_word = "hello siri"
        recognizer = sr.Recognizer()
        recognizer.dynamic_energy_threshold = True
        mic = sr.Microphone()

        print("Listening...")

        while True:
            with mic as source:
                # TODO: adjust for ambient noise so it does not mishear background sounds
                recognizer.adjust_for_ambient_noise(source, duration=1)


                # TODO: listen for audio input
                audio = recognizer.listen(source)

            try:
                #TODO: convert audio to text using Google's free speech recognition
                text = recognizer.recognize_google(audio)
                print(f"Heard: {text}")

                #TODO: check if the wake word is in the text
                # if it is, extract the command and call on_command()
                if wake_word in text.lower():
                    command = text.lower().replace(wake_word, "").strip()
                    on_command(command)

            except sr.UnknownValueError:
                pass #couldn't understand audo -> keep listening later change to error msg
            except sr.RequestError as e:
                print(f"API Error: {e}")
        
    thread = threading.Thread(target=listen_loop, daemon=True) # daemon thread -> dies automatically when main program exits
    thread.start()