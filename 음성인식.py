# pip install SpeechRecognition
# pip install PyAudio [wheel download(https://pypi.bartbroe.re/pyaudio/)]
from speech_recognition import Microphone, Recognizer

recog = Recognizer()
mic = Microphone()

with mic:
    print("말해")
    audio = recog.listen(mic, 3)

reconized = recog.recognize_google(audio)
print(f"말한 내용은 : {reconized}")