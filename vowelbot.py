#coding=utf-8
import os
import random
import time
import datetime

import twitter

g_srcWordsFile = 'wordlist.txt'
g_srcVoweledFile = 'vowelwords.csv'
g_voweledProgressFile = 'vowellist.csv'

VOWELS = 'aeiou'

# vowel file generation ------------------------------------------------------

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

# bot utility stuff ---------------------------------------------------------

def make_words_from_selection(opt):
    data = opt.split(',')
    word, vowels = data[0], data[1:]
    return [word.replace('*', v) for v in vowels]

def load_vowellist():
    vowelfile = g_voweledProgressFile
    if not os.path.exists(vowelfile):
        make_vowel_file(outfile=vowelfile)
    with open(vowelfile) as vowellist_f:
        vowellist = vowellist_f.readlines()
    vowellist = map(str.strip, vowellist)
    return vowellist

def save_updated_vowellist(vowellist):
    with open(g_voweledProgressFile, 'w+') as vowelscratch_f:
        vowelscratch_f.writelines(vowellist)


class VowelPollBot(object):

    _auth_file = 'vowelbot.auth'

    TIME_BETWEEN_TWEETS = datetime.timedelta(hours=13, minutes=4, seconds=20)  # who cares

    @staticmethod
    def get_auth_tokens():
        with open(VowelPollBot._auth_file) as auth_f:
            auth_data = auth_f.read()
        return auth_data.split()

    @staticmethod
    def save_auth_tokens(access_token, access_secret, cons_key, cons_secret):
        with open(VowelPollBot._auth_file, 'w') as auth_f:
            auth_f.write('\n'.join([access_token, access_secret, cons_key, cons_secret]))

    def __init__(self):
        self.oauth = None
        self.twitter = None
        self.credentials = None

    def login(self):
        token, token_secret, consumer_key, consumer_secret = VowelPollBot.get_auth_tokens()
        self.oauth = twitter.OAuth(token, token_secret, consumer_key, consumer_secret)
        self.twitter = twitter.Twitter(auth=self.oauth)
        self.credentials = self.twitter.account.verify_credentials()

    def run(self, oneoff=False):
        vowellist = load_vowellist()
        while True:

            ok_to_post = False
            candidate = resp = ''
            while not ok_to_post:
                candidate = random.choice(vowellist)
                word_and_opts = make_words_from_selection(candidate)
                resp = self.make_tweet(word_and_opts)
                if len(resp) < 140:
                    ok_to_post = True

            self.post_tweet(resp)

            vowellist.remove(candidate)  # prevent duplicates
            save_updated_vowellist(vowellist)

            if oneoff:
                break

            print "zzzzzzzz"
            time.sleep(VowelPollBot.TIME_BETWEEN_TWEETS.total_seconds())

    @staticmethod
    def make_fixedwidth(word):
        fixedletters = u"ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
        mapper = lambda c: ord(c) - ord('a')
        indeces = map(mapper, word)
        return u''.join(fixedletters[i] for i in indeces)


    @staticmethod
    def make_tweet(words):
        base_word = VowelPollBot.make_fixedwidth(words[0])
        poll_opts = map(VowelPollBot.make_fixedwidth,words[1:])
        random.shuffle(poll_opts)

        # ok so we can't make a poll. just post something
        fmts = (
unicode(ur"""┏{line:━^{bwidth}}━┓
┃{base:　^{bwidth}}　┃
┗┳{line:━^{bwidth}}┛
　┣{0}
　┣{1}
　┣{2}
　┗{3}"""),
unicode(ur"""╭{line:─^{bwidth}}─╮
│{base:　^{bwidth}}　│
╰┬{line:─^{bwidth}}╯
　├{0}
　├{1}
　├{2}
　╰{3}"""),
# unicode(ur"""▛{line:▀^{bwidth}}▀▜
# ▌{base:　^{bwidth}}　▐
# ▙▞{line:▄^{bwidth}}▟
# 　▗{0}
# 　▗{1}
# 　▗{2}
# 　▙{3}"""),  this one looks ugly and I'm tired
        )
        fmt = random.choice(fmts)
        msg = fmt.format(base=base_word, line=u'', bwidth=len(base_word), *poll_opts)
        return msg

    def post_tweet(self, msg):
        self.twitter.statuses.update(status=msg)




def main():
    if not os.path.exists(g_srcVoweledFile):
        make_vowel_file(g_srcWordsFile, g_srcVoweledFile)

    print "Here's some stuff"
    # sduhuuhfhhgfbjg
    with open(g_srcVoweledFile) as funtown:
        vowellist = funtown.readlines()
    vowellist = map(str.strip, vowellist)
    print VowelPollBot.make_tweet(make_words_from_selection(random.choice(vowellist)))

if __name__ == "__main__":
    main()