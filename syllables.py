import string


def get_syllables(word):
    """Returns the number of syllables in a word."""
    vowels = "aeiouy"
    syl_count = 0
    for p in string.punctuation.replace('-',''):
        word = word.replace(p, '')
    word = word.replace('-', ' ')
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


def is_haiku(string):
    haiku = string.split("\n")
    p1_sum = p2_sum = p3_sum = 0
    for wd in haiku[0].strip().split():
        p1_sum += get_syllables(wd)
    print(p1_sum)
    for wd in haiku[1].strip().split():
        p2_sum += get_syllables(wd)
    print(p2_sum)
    for wd in haiku[2].strip().split():
        p3_sum += get_syllables(wd)
    print(p3_sum)
    if p1_sum == 5 and p2_sum == 7 and p3_sum == 5:
        return True
    return False


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
    is_haiku("Autumn moonlight\na worm digs silently\ninto the chestnut.") is True
    print("All tests passed.")
    input()
