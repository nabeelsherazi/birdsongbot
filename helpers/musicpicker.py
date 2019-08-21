import random
randomizer = random.Random()

moods = ['low', 'medlow', 'med', 'medhi', 'hi']
intro_sounds = ['IntroSound1', 'IntroSound2', 'IntroSound3']

def get_music_names(l1_sent_num, l2_sent_num, l3_sent_num):
	# For each sentiment, we pick the mood
	l1_mood = moods[l1_sent_num]
	l2_mood = moods[l1_sent_num]
	l3_mood = moods[l3_sent_num]
	# Within each mood, we pick a random phrase
	l1_phrase = randomizer.randint(1, 14)
	l2_phrase = l1_phrase
	# Make sure we don't use the same phrase multiple times
	while l2_phrase == l1_phrase:
		l2_phrase = randomizer.randint(1, 14)
	l3_phrase = l2_phrase
	while l3_phrase == l2_phrase or l3_phrase == l1_phrase:
		l3_phrase = randomizer.randint(1, 14)
	# Assemble the final filenames to be played
	l1_music = 'p' + str(l1_phrase) + str(l1_mood)
	l2_music = 'p' + str(l2_phrase) + str(l2_mood)
	l3_music = 'p' + str(l3_phrase) + str(l3_mood)
	return (l1_music, l2_music, l3_music)

def get_intro():
	# Play a random intro
    choice = intro_sounds[random.Random().randint(0, 2)]
    return choice
