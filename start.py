import tweepy
import json
import time
import sys
import indicoio
import pygame
import pyttsx3
import signal
from subprocess import Popen, PIPE
from helpers import musicpicker, syllables
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
config = config["DEFAULT"]

try:
    # Program settings
    rejected_mode = config.getboolean("REJECTED_MODE")
    bot_username = config["TWITTER_USERNAME"]
    filter_bad_words = config.getboolean("FILTER_BAD_WORDS")

    # Authentication details for twitter and indicoio
    consumer_key = config["TWITTER_CONSUMER_KEY"]
    consumer_secret = config["TWITTER_CONSUMER_SECRET"]
    access_token = config["TWITTER_ACCESS_TOKEN"]
    access_token_secret = config["TWITTER_ACCESS_TOKEN_SECRET"]
    indicoio.config.api_key = config["INDICO_API_KEY"]
except KeyError as e:
    print(f"Error! Missing {str(e)}")
    print("Have you added your API keys to config.ini?")
    sys.exit()

if filter_bad_words:
    try:
        with open("helpers/bad-words.txt", "r") as f:
            bad_words_list = f.read().splitlines()
    except:
        print("Missing bad words file. Add back helpers/bad_words.txt and restart.")
        sys.exit()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Init pygame, which will handle playing music
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

# Start the TTS engine process

engine_process = Popen(["python", "helpers/ttsengine.py"], stdin=PIPE)


def speak(sentence):
    engine_process.stdin.write(f"{sentence}\n".encode())
    engine_process.stdin.flush()


speak("Starting Birdsong!")


# This is the listener, responsible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):

        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        tweet_haiku = decoded['text'].replace(f'@{bot_username}', "").lstrip()
        tweet_name = decoded['user']['screen_name']

        # Syllable checking is gonna happen right here
        # Syllable module checks if haiku is really a haiku, we're gonna play error sound if not

        if filter_bad_words and any(word in bad_words_list for word in tweet_haiku.split()):
            # Someone sent a haiku with a bad word in it!!
            print("Received inappropriate haiku")
            print(tweet_haiku)
            print("Skipping")
            return True

        is_haiku = syllables.is_haiku(tweet_haiku)

        print(tweet_haiku)

        if not is_haiku and rejected_mode is True:
            # If it's not a haiku.... shame!!!
            speak("Haiku submitted by user " + tweet_name)
            pygame.mixer.music.load("sounds/ErrorSound.mp3")
            pygame.mixer.music.play()
            speak("That is not a haiku my friend")

        else:
            # Introduction to haiku
            intro_sound = musicpicker.get_intro()
            pygame.mixer.music.load(f"sounds/{intro_sound}.mp3")
            pygame.mixer.music.play()
            time.sleep(1.2)
            speak("Haiku Submitted by user " + tweet_name)

            # Assuming everything is good
            # Split tweet into an array
            tweet_text_array = decoded['text'].replace(
                "@birdsongbot", "").replace("\"", "").replace("\'", "").split('\n')

            # INDICO SENTIMENT JAZZ

            sentiments = indicoio.sentiment(tweet_text_array)
            sentiments = tuple(map(lambda x: int(x * 5), sentiments))

            fileNames = musicpicker.get_music_names(sentiments)
            print(f"Playing {fileNames}")

            for i in range(3):
                # Load and play the music
                pygame.mixer.music.load(f"sounds/{fileNames[i]}.wav")
                pygame.mixer.music.play()
                # Reading the Haiku line with macs sweet sweet voice
                speak(tweet_text_array[i])
                time.sleep(1)

            time.sleep(3)
        return True

    def on_error(self, status):
        print(status)


def exit_handler(signum, frame):
    print("Exiting Birdsong")
    stream.disconnect()
    engine_process.kill()
    sys.exit(0)


if __name__ == '__main__':
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    print(f"Listening at @{bot_username}:")
    signal.signal(signal.SIGINT, exit_handler)
    print('Press Ctrl+C to stop the bot on next keep-alive (within 15ish seconds)')
    print('ONLY exit the bot via Ctrl+C to properly close the stream and TTS engine.')
    print('Otherwise you may have orphaned processes floating around.')
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=[f'@{bot_username}'])
