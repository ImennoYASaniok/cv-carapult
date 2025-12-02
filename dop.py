from voice import voice
import time

words_codes = [
    ("выстрел", 1)
]

voice = voice(25, words_codes)

while True:
    time.sleep(10)