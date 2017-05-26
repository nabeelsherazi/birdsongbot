import string


def get_syllables(word):
    """Returns the number of syllables in a word."""
    vowels = "aeiouy"
    syl_count = 0
    for p in string.punctuation:
        word = word.replace(p, '')
    word = word.lower()
    for ix in range(0, len(word)):
        if ix == 0:
            if word[ix] in vowels:
                syl_count += 1
        else:
            if word[ix] in vowels and word[ix - 1] not in vowels:
                syl_count += 1
    if word.endswith('e'):
        syl_count -= 1
    if word.endswith('le') or word.endswith('re'):
        syl_count += 1
    if syl_count == 0:
        syl_count = 1
    return syl_count


if __name__ == '__main__':
    assert get_syllables('eat') == 1
    assert get_syllables('refrigerator') == 5
    assert get_syllables('bicycle') == 3
    assert get_syllables('alimony') == 4
    assert get_syllables('read') == 1
    assert get_syllables('oolong') == 2
    assert get_syllables('laboratory') == 5
    assert get_syllables('every') == 3
    assert get_syllables('dIffEreNt') == 3
    assert get_syllables('&stra!nge.') == 1
    print("All tests passed.")
    input()
