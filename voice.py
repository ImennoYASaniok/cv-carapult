from threading import Thread
import json, pyaudio, time
from vosk import Model, KaldiRecognizer
from get_code_from_text import return_code_from_text



class voice():

    def __init__(self, credulity, WordsCodes):
        self.text = ""
        self.credulity = credulity
        self.IsActive = True
        self.audio_data = None
        self.model = Model("small_model")
        self.rec = KaldiRecognizer(self.model, 16000)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.stream.start_stream()
        self.words = WordsCodes
        Thread(target=self.main).start()


    def main(self):
        while True:
            if self.IsActive:
                self.stream.start_stream()
                self.text = self.recognize_speech()
                self.do_anything_with_code(return_code_from_text(text=self.text, credulity=self.credulity, words=self.words))
            else:
                self.stream.stop_stream()
                time.sleep(5)

    def recognize_speech(self):
        while self.IsActive:
            data = self.stream.read(4000, exception_on_overflow=False)
            if (self.rec.AcceptWaveform(data)) and (len(data) > 0):
                answer = json.loads(self.rec.Result())
                if answer["text"]:
                    print(answer["text"])
                    return answer["text"]
        return "-1"

    def activate(self):
        self.IsActive = True

    def deactivate(self):
        self.IsActive = False


    def do_anything_with_code(self, code):
        print(code)