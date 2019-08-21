import tweepy
import json
import os
import time
import sys
import indicoio
import pygame
from helpers import musicpicker
from helpers import syllables
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

try:
    # Program settings
    rejected_mode = config["DEFAULT"].getboolean("REJECTED_MODE")
    bot_username = config["TWITTER_USERNAME"]
    filter_bad_words = config["DEFAULT"].getboolean("FILTER_BAD_WORDS")

    # Authentication details for twitter and indicoio
    consumer_key = config["TWITTER_CONSUMER_KEY"]
    consumer_secret = config["TWITTER_CONSUMER_SECRET"]
    access_token = config["TWITTER_ACCESS_TOKEN"]
    access_token_secret = config["TWITTER_TOKEN_SECRET"]
    indicoio.config.api_key = config["INDICO_API_KEY"]
except KeyError as e:
    print(f"Error! Missing {str(e)}")
    print("Have you added your API keys to config.ini?")
    sys.exit()

if filter_bad_words:
    try:
        with open("helpers/bad_words.txt") as f:
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

# Get what system we're on to determine how to handle TTS
current_system = sys.platform
if current_system == "win32":
    def speak(sentence):
        os.system(f'powershell .\\scripts\\speak.ps1 "{sentence}"')
elif current_system == "darwin" or current_system == "linux":
    def speak(sentence):
        os.system(f'say "{sentence}"')
else:
    print("OS not recognized. Unable to speak.")
    sys.exit()


# This is the listener, resposible for receiving data
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
            sentimentVal1 = indicoio.sentiment(tweet_text_array[0])
            sentimentVal1 = int(sentimentVal1 * 5)

            sentimentVal2 = indicoio.sentiment(tweet_text_array[1])
            sentimentVal2 = int(sentimentVal2 * 5)

            sentimentVal3 = indicoio.sentiment(tweet_text_array[2])
            sentimentVal3 = int(sentimentVal3 * 5)

            fileNames = musicpicker.get_music_names(
                sentimentVal1, sentimentVal2, sentimentVal3)
            print(f"Playing {fileNames}")

            # Load and play the music for line 1
            pygame.mixer.music.load("sounds/{0}.wav".format(fileNames[0]))
            pygame.mixer.music.play()

            # Reading Haiku line 1 with macs sweet sweet voice
            speak(tweet_text_array[0])
            print()

            time.sleep(1)

            # Load and play the music for line 2
            pygame.mixer.music.load("sounds/{0}.wav".format(fileNames[1]))
            pygame.mixer.music.play()

            # Reading Haiku line 2 with macs sweet sweet voice
            speak(tweet_text_array[1])
            print()

            time.sleep(1)

            # Load and play the music for line 3
            pygame.mixer.music.load("sounds/{0}.wav".format(fileNames[2]))
            pygame.mixer.music.play()

            # Reading Haiku line 3 with macs sweet sweet voice
            speak(tweet_text_array[2])
            print()
            time.sleep(3)

        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    print(f"Showing all new tweets for @{bot_username}:")
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=[f'@{bot_username}'])
