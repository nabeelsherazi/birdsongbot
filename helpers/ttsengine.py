import pyttsx3
import sys

engine = pyttsx3.init()

while True:
    input = sys.stdin.readline()
    if input:
        engine.say(input)
        engine.runAndWait()
