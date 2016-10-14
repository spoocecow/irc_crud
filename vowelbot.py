import os
import random

g_srcWordsFile = 'wordlist.txt'
g_srcVoweledFile = 'vowelwords.csv'
g_voweledProgressFile = 'vowellist.csv'

VOWELS = 'aeiou'

def has_one_vowel(word):
    vc = 0
    if word[0].isupper():
        return False  # NO PROPER NOUNS PLEASE!!!!!
    for letter in word:
        if letter.lower() in VOWELS:
            vc += 1
            if vc > 1:
                return False
    # OPEN QUESTION: is y a vowel........................?
    return vc == 1

def get_vowel(word):
    for letter in word:
        if letter.lower() in VOWELS:
            return letter.lower()
    exit("I have failed to write code goodly.")

def get_neighbor_vowels(vowel):
    return VOWELS.replace(vowel, '')

def get_neighbor_words(word):
    myvowel = get_vowel(word)
    neighbor_vowels = get_neighbor_vowels(myvowel)
    return [word.replace(myvowel, newvowel) for newvowel in neighbor_vowels]

def has_no_neighbors(word, all_words):
    neighbor_words = get_neighbor_words(word)
    for neighbor in neighbor_words:
        if neighbor in all_words:
            return False
    return True

def get_writeable_str(word):
    vowel = get_vowel(word)
    neighbor_vowels = get_neighbor_vowels(vowel)
    return '{word},{vowel},{},{},{},{}'.format(word=word.replace(vowel,'*'), vowel=vowel, *neighbor_vowels)

def make_vowel_file(wordlist_src=g_srcWordsFile, outfile=g_srcVoweledFile):
    """
    Transform list of words to make list of one-vowel, no-neighbor words.
    :param wordlist_src: path to list of english words
    :param outfile: path to write list of pollable words
    """
    with open(wordlist_src, 'r') as wordlist_f:
        wordlist = wordlist_f.readlines()

    # 1. pare list down to words with one vowel
    good_words = []
    for word in wordlist:
        if has_one_vowel(word):
            good_words.append(word.strip())

    # 2. pare further to words whose vowel doesn't form another word if changed
    # (e.g. BURP is good because BARP, BERP, BIRP, and BORP are [regrettably] not words)
    final_words = []
    for word in good_words:
        if has_no_neighbors(word, good_words):
            final_words.append(word)

    # Write final list of words, specially formatted, to outfile
    with open(outfile, 'w+') as out_f:
        for word in final_words:
            wordstr = get_writeable_str(word)
            out_f.write(wordstr + '\n')

    return final_words


def get_next_selection(vowellist):
    opt = random.choice(vowellist)
    data = opt.split(',')
    word, vowels = data[0], data[1:]

    return [word.replace('*', v) for v in vowels]

def main():
    if not os.path.exists(g_srcVoweledFile):
        make_vowel_file(g_srcWordsFile, g_srcVoweledFile)

    print "Here's some stuff"
    # sduhuuhfhhgfbjg
    with open(g_srcVoweledFile) as funtown:
        vowellist = funtown.readlines()
    vowellist = map(str.strip, vowellist)
    for _ in range(5):
        realword = ''
        words = []
        while len(realword) <= 4:
            words = get_next_selection(vowellist)
            realword = words[0]

        fakewords = words[1:]
        random.shuffle(fakewords)
        print realword.upper()
        for i, fakeword in enumerate(fakewords):
            print '\t%d.' % (i+1), fakeword.upper()
        print

if __name__ == "__main__":
    main()