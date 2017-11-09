import tweepy, json
import os, time, authkeys
import sys
import indicoio
import pygame, musicpicker, syllables

# Reject mode announces people who didn't write a haiku correctly.
rejected_mode = True

# Authentication details for twitter and indicoio
consumer_key = authkeys.consumer_key
consumer_secret = authkeys.consumer_secret
access_token = authkeys.access_token
access_token_secret = authkeys.access_token_secret
indicoio.config.api_key = authkeys.indico_key

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Init pygame, which will handle playing music
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

# Get what system we're on to determine how to handle TTS
current_system = sys.platform


speak_command = {"win32": "powershell tts\\.\\speak.ps1 '{}'", "darwin": "say '{}'", "linux": "say '{}'"}


# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):

        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        tweet_haiku = decoded['text'].replace("@birdsongbot","").lstrip()
        tweet_name = decoded['user']['screen_name']

        # Syllable checking is gonna happen right here
        # Syllable module checks if haiku is really a haiku, we're gonna play error sound if not

        is_haiku = syllables.is_haiku(tweet_haiku)
        print(tweet_haiku)

        if is_haiku is False and rejected_mode is True:
            os.system(speak_command[current_system].format("Submitted by user " + tweet_name))
            pygame.mixer.music.load("sounds/ErrorSound.mp3")
            pygame.mixer.music.play()
            os.system(speak_command[current_system].format("That is not a haiku my friend"))

        else:
            # Do the stuff to make it say that its not a haiku
            # Write code here to make it go back to listening immediately

            # Introduction to haiku
            pygame.mixer.music.load("sounds/IntroSound1.mp3")
            pygame.mixer.music.play()
            time.sleep(1.2)
            os.system(speak_command[current_system].format("Submitted by user " + tweet_name))



            # Assuming everything is good
            # Split tweet into an array
            tweet_text_array = decoded['text'].replace("@birdsongbot","").replace("\"", "").replace("\'", "").split('\n')

            # INDICO SENTIMENT JAZZ
            sentimentVal1 = indicoio.sentiment(tweet_text_array[0])
            sentimentVal1 = int(sentimentVal1 * 5)

            sentimentVal2 = indicoio.sentiment(tweet_text_array[1])
            sentimentVal2 = int(sentimentVal2 * 5)

            sentimentVal3 = indicoio.sentiment(tweet_text_array[2])
            sentimentVal3 = int(sentimentVal3 * 5)

            fileNames = musicpicker.get_music_names(sentimentVal1, sentimentVal2, sentimentVal3)
            print(fileNames)


            #Load and play the music for line 1
            pygame.mixer.music.load("sounds/{0}.wav".format(fileNames[0]))
            pygame.mixer.music.play()

            #Reading Haiku line 1 with macs sweet sweet voice
            os.system(speak_command[current_system].format(tweet_text_array[0]))
            print()

            time.sleep(1)

            #Load and play the music for line 2
            pygame.mixer.music.load("sounds/{0}.wav".format(fileNames[1]))
            pygame.mixer.music.play()

            #Reading Haiku line 2 with macs sweet sweet voice
            os.system(speak_command[current_system].format(tweet_text_array[1]))
            print()

            time.sleep(1)

            #Load and play the music for line 3
            pygame.mixer.music.load("sounds/{0}.wav".format(fileNames[2]))
            pygame.mixer.music.play()

            #Reading Haiku line 3 with macs sweet sweet voice
            os.system(speak_command[current_system].format(tweet_text_array[2]))
            print()
            time.sleep(3)

        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    print("Showing all new tweets for @birdsongbot:")

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['@birdsongbot'])
