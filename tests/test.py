import unittest
import os
import sys

# Idk why this is broken
if "tests" in os.getcwd():
    sys.path.append(os.path.abspath('../helpers/'))
    import musicpicker
    import syllables
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

    print("Testing music picker library. This needs to be improved.")
    l1_test = int(input('l1sent = '))
    l2_test = int(input('l2sent = '))
    l3_test = int(input('l3sent = '))
    print(musicpicker.get_music_names(l1_test, l2_test, l3_test))
    input()

    print("All tests passed.")
    input()
