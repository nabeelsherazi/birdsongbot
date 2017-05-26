import random
randomizer = random.Random()

def get_music_names(l1_sent_num, l2_sent_num, l3_sent_num):
	moods = ['low', 'medlow', 'med', 'medhi', 'hi']
	l1_mood = moods[l1_sent_num]
	l2_mood = moods[l1_sent_num]
	l3_mood = moods[l3_sent_num]
	l1_phrase = randomizer.randint(1, 14)
	l2_phrase = l1_phrase
	while l2_phrase == l1_phrase:
		l2_phrase = randomizer.randint(1, 14)
	l3_phrase = l2_phrase
	while l3_phrase == l2_phrase or l3_phrase == l1_phrase:
		l3_phrase = randomizer.randint(1, 14)
	l1_music = 'p' + str(l1_phrase) + str(l1_mood)
	l2_music = 'p' + str(l2_phrase) + str(l2_mood)
	l3_music = 'p' + str(l3_phrase) + str(l3_mood)
	return (l1_music, l2_music, l3_music)

if __name__ == "__main__":
	l1_test = int(input('l1sent = '))
	l2_test = int(input('l2sent = '))
	l3_test = int(input('l3sent = '))
	print(get_music_names(l1_test, l2_test, l3_test))
	input()

def get_intro():
    introSound = ['IntroSound1','IntroSound2','IntroSound3']
    choice = random.Random().randint(0,2)
    introSound[choice]
    return introSound[choice]