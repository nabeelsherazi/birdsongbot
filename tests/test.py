import unittest
import os
import sys
import random
import json

rnd = random.Random()

# Idk why this is broken
if "tests" in os.getcwd():
    sys.path.append(os.path.abspath('../helpers/'))
    sys.path.append(os.path.abspath('../'))
    import musicpicker
    import syllables
    from start import *
else:
    print("Call this from the tests folder pls.")
    sys.exit()

if __name__ == '__main__':
    print("Testing syllables library")
    assert syllables.get_syllables('eat') == 1
    assert syllables.get_syllables('refrigerator') == 5
    assert syllables.get_syllables('bicycle') == 3
    assert syllables.get_syllables('alimony') == 4
    assert syllables.get_syllables('read') == 1
    assert syllables.get_syllables('oolong') == 2
    assert syllables.get_syllables('laboratory') == 5
    assert syllables.get_syllables('every') == 3
    assert syllables.get_syllables('dIffEreNt') == 3
    assert syllables.get_syllables('&stra!nge.') == 1
    assert syllables.is_haiku(
        "Autumn in moonlight\na pink worm digs silently\ninto the chestnut.") is True

    print("Testing music picker library. Enter values in range 1-5. This needs to be improved.")

    music_list = musicpicker.get_music_names((rnd.randint(1, 5), (rnd.randint(1, 5), (rnd.randint(1, 5))
    assert len(filter(None, music_list)) == 3

    print("Testing haiku processor")

    print("All tests passed.")
    input()
