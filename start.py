import tweepy
import json
import time
import sys
import indicoio
import os
import pygame
import pyttsx3
import signal
import string
import atexit
import time
from tinydb import TinyDB, Query
from subprocess import Popen, PIPE
from helpers import musicpicker, syllables
import configparser
import logging
from logging.handlers import RotatingFileHandler

# Register exit handler first in case something goes wrong


def exit_handler(signum=None, frame=None):
    log.info("Cleaning up before exit")
    try:
        stream.disconnect()
    except NameError:
        log.info("Stream never opened so no need to close.")
    else:
        log.info("Stream closed succesfully")
    try:
        engine_process.kill()
    except NameError:
        log.info("TTS engine never started so no need to kill")
    else:
        log.info("TTS engine stopped successfully")
    log.info("Exiting Birdsong!")


def exit(signum=None, frame=None):
    sys.exit(0)


atexit.register(exit_handler)

# Setup logger
log_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s')

logFile = 'logs/app.log'

os.makedirs("logs", exist_ok=True)
file_handler = RotatingFileHandler(logFile, mode='a+', maxBytes=5*1024*1024,
                                   backupCount=1, encoding=None, delay=0)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

log = logging.getLogger('root')
log.setLevel(logging.INFO)

log.addHandler(file_handler)
log.addHandler(stream_handler)

log.info("Begin logging...")

# Read config variables

config = configparser.ConfigParser()
try:
    config.read("config.ini")
except:
    log.error(
        "Config file not found. Did you follow the instructions in the template file?")
    sys.exit()
else:
    config = config["DEFAULT"]

try:
    # Program settings
    rejected_mode = config.getboolean("REJECTED_MODE")
    bot_username = config["TWITTER_USERNAME"]
    filter_bad_words = config.getboolean("FILTER_BAD_WORDS")
    max_strikes = config.getint("MAX_STRIKES")
    cooldown_period = config.getint("COOLDOWN_PERIOD")

    # Authentication details for twitter and indicoio
    consumer_key = config["TWITTER_CONSUMER_KEY"]
    consumer_secret = config["TWITTER_CONSUMER_SECRET"]
    access_token = config["TWITTER_ACCESS_TOKEN"]
    access_token_secret = config["TWITTER_ACCESS_TOKEN_SECRET"]
    indicoio.config.api_key = config["INDICO_API_KEY"]
except KeyError as e:
    log.error(f"Error! Missing {str(e)}")
    log.error("Have you added your API keys to config.ini?")
    sys.exit()

# Set up DB
os.makedirs("db", exist_ok=True)
db = TinyDB("db/db.json")

# Bad words filter
if filter_bad_words:
    try:
        with open("helpers/bad-words.txt", "r") as f:
            bad_words_list = f.read().splitlines()
    except:
        log.error(
            "Missing bad words file. Add back helpers/bad_words.txt and restart.")
        sys.exit()

# Set up stream auth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Init pygame, which will handle playing music
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

# Start the TTS engine process
try:
    engine_process = Popen(["python", "helpers/ttsengine.py"], stdin=PIPE)
except:
    log.error("Unable to start TTS engine. Exiting.")
    sys.exit()
else:
    # Speak can only work if engine_process is defined so...
    def speak(sentence):
        log.info(sentence)
        engine_process.stdin.write(f"{sentence}\n".encode())
        engine_process.stdin.flush()


def make_yellow(strg):
    return '\033[93m' + strg + '\033[0m'


speak("Starting Birdsong!")


# This is the listener, responsible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):

        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        tweet_haiku = decoded['text'].replace(f'@{bot_username}', "").lstrip()
        sender_name = decoded['user']['screen_name']

        # Control spammers
        user = Query()
        # If we've seen this user before, check if banned or are sending too much
        user_data = db.search(user.name == sender_name)
        if user_data:
            if user_data["strikes"] >= max_strikes:
                # Can you hear me, Twitter account with the three strikes?
                db.update({"last_seen": time.time(
                ), "times_sent": user_data["times_sent"] + 1}, user.name == sender_name)
                log.info(
                    f"Banned user {sender_name} tried to send again. Eyeroll.")
                return True
            elif time.time() - user_data["last_seen"] < cooldown_period:
                db.update({"last_seen": time.time()}, user.name == sender_name)
                log.info(f"User {sender_name} sending too much. Chill out.")
                return True
            else:
                # Update them and send them on their merry way
                db.update({"times_sent": user_data["times_sent"] + 1,
                           "last_seen": time.time()}, user.name == sender_name)
        else:
            # Haven't seen them before. Start tracking.
            user_data = {"name": sender_name,
                         "last_seen": time.time(), "times_sent": 0, "strikes": 0}
            db.insert(user_data)

        # Syllable checking is gonna happen right here
        # Syllable module checks if haiku is really a haiku, we're gonna play error sound if not

        if filter_bad_words and any(word in bad_words_list for word in tweet_haiku.split()):
            # Someone sent a haiku with a bad word in it!!
            log.info("Received inappropriate haiku")
            log.info(tweet_haiku)
            log.info(f"Adding strike to user {sender_name} and skipping")
            db.update(
                {"strikes": user_data["strikes"] + 1}, user.name == sender_name)
            if user_data["strikes"] + 1 > max_strikes:
                log.info("You're out! User was banned.")
            return True

        # At this stage, haiku is single string broken by newlines
        is_haiku = syllables.is_haiku(tweet_haiku)

        if not is_haiku and rejected_mode is True:
            # If it's not a haiku.... shame!!!
            speak("Haiku submitted by user " + sender_name)
            pygame.mixer.music.load("sounds/ErrorSound.mp3")
            pygame.mixer.music.play()
            speak("That is not a haiku my friend")

        else:
            # Introduction to haiku
            intro_sound = musicpicker.get_intro()
            pygame.mixer.music.load(f"sounds/{intro_sound}.mp3")
            pygame.mixer.music.play()
            time.sleep(1.2)
            speak("Haiku Submitted by user " + sender_name)

            # Assuming everything is good
            # Strip all punctuation and split tweet into an array
            tweet_haiku = tweet_haiku.translate(
                str.maketrans('', '', string.punctuation))
            haiku_line_list = tweet_haiku.split('\n')
            # Remove any empty elements from list (caused by extra newlines)
            haiku_line_list = list(filter(None, haiku_line_list))
            if len(haiku_line_list) != 3:
                log.debug("Something went wrong with haiku:")
                log.debug(haiku_line_list)
                return True

            # INDICO SENTIMENT JAZZ
            sentiments = indicoio.sentiment(haiku_line_list)
            sentiments = tuple(map(lambda x: int(x * 5), sentiments))

            fileNames = musicpicker.get_music_names(sentiments)
            log.info(f"Playing {fileNames}")

            for i in range(3):
                # Load and play the music
                pygame.mixer.music.load(f"sounds/{fileNames[i]}.wav")
                pygame.mixer.music.play()
                # Reading the Haiku line with macs sweet sweet voice
                speak(haiku_line_list[i])
                time.sleep(1)

            time.sleep(3)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    log.info(f"Listening at @{bot_username}:")
    signal.signal(signal.SIGINT, exit)
    print(make_yellow(
        'Press Ctrl+C to stop the bot on next keep-alive (within 15ish seconds)'))
    print(make_yellow(
        'ONLY exit the bot via Ctrl+C to properly close the stream and TTS engine.'))
    print(make_yellow('Otherwise you may have orphaned processes floating around.'))
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=[f'@{bot_username}'])
