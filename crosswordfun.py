import functools
import os
import random
import sys
import time


def memoize(func):
    cache = dict()
    @functools.wraps(func)
    def inner(*args, **kwargs):
        h = hash(args)
        if h in cache:
            return cache[h]
        rv = func(*args, **kwargs)
        cache[hash(args)] = rv
        return rv
    return inner


def cls():
    #print('\033[H\033[J')
    os.system('clear')


g_letters = 'abcdefghijklmnopqrstuvwxyz'
g_corp = []

L = {l: [] for l in g_letters}  # words indexed by letter/space
M = {l: [] for l in g_letters}  # probability of letter at space
MM = {l: 0 for l in g_letters}  # probability of letter overall
W = dict()  # words indexed by length

def setup():
    global g_corp
    global L
    global M
    global MM
    global W
    with open(r'C:\Users\Mark\Documents\GitHub\irc_crud\wordlist.txt') as t:
        g_corp = [w.strip().lower() for w in t.readlines()]

    print sys.getsizeof(L)

    t = time.time()

    for word in g_corp:
        if len(word) not in W:
            W[len(word)] = []
        W[len(word)].append(word)
        for i, letter in enumerate(word):
            while len(L[letter]) <= i:
                L[letter].append( [] )
            L[letter][i].append(word)
            MM[letter] += 1

    for letter in L:
        places = L[letter]
        all_places = sum(map(len, places))
        M[letter] = [0] * len(places)
        for i, p in enumerate(places):
            M[letter][i] = len(places[i]) / float(all_places)

    print time.time() - t, sys.getsizeof(L)

def words_with_letter(letter, place):
    return set(L[letter][place])

@memoize
def words_that_fit(template):
    # special case: no letters filled in at all
    if template == '_' * len(template):
        return W[len(template)]

    rv = []
    for i, letter in enumerate(template):
        if letter not in g_letters:
            continue
        s = words_with_letter(letter, i)
        s2 = s.copy()
        for w in s2:
            if len(w) != len(template):
                s.discard(w)
        if len(s) > 0:
            rv.append(s)
        else:
            return []
    final = rv[0]
    assert isinstance(final, set)
    for s in rv[1:]:
        final.intersection_update(s)
        if len(final) == 0:
            return []
    return final

@memoize
def score(template):
    total = 0
    mmratio = float(sum(MM.values()))
    for i, letter in enumerate(template):
        if letter == '_':
            continue
        if len(M[letter]) <= i:
            return -1
        total += (M[letter][i] * (MM[letter] / mmratio))
    return total

class Grid(object):

    ACROSS = 0
    DOWN = 1

    MIN_WORD_LEN = 1

    def __init__(self, grid=''):
        self.G = grid.splitlines()
        if not grid:
            self.G = \
"""
##___
#____
_____
____#
___##
""".splitlines()
        self.G = filter(None, self.G)
        self.H = len(self.G)
        self.W = len(self.G[0])
        self.across_starts, self.down_starts = [], []
        self.across_coords, self.down_coords = [], []
        self.across_words, self.down_words = [], []
        self.words = dict()
        self.__find_starts()
        self.__find_words()

    def __find_starts(self):
        for y, row in enumerate(self.G):
            for x, col in enumerate(row):
                if col != '#':
                    if x == 0 or (x >= 1 and self.at(x-1, y) == '#'):
                        self.across_starts.append( (x, y) )
                    if y == 0 or (y >= 1 and self.at(x, y-1) == '#'):
                        self.down_starts.append( (x, y) )

    def at(self, x, y):
        return self.G[y][x]

    def __find_words(self):
        self.across_words = []
        self.down_words = []
        self.words = dict()
        for across_start in self.across_starts:
            x, y = across_start
            w = ''
            coords = []
            while x < self.W and self.at(x, y) != '#':
                w += self.at(x,y)
                coords.append( (x,y) )
                x += 1
            if len(w) >= Grid.MIN_WORD_LEN:
                self.across_words.append(w)
                self.across_coords.append(coords)
            for coord in coords:
                self.words[coord] = [w]
        for down_start in self.down_starts:
            x, y = down_start
            w = ''
            coords = []
            while y < self.H and self.at(x, y) != '#':
                w += self.at(x, y)
                coords.append( (x, y) )
                y += 1
            if len(w) >= Grid.MIN_WORD_LEN:
                self.down_words.append(w)
                self.down_coords.append(coords)
            for coord in coords:
                self.words[coord].append(w)

    def get_start_of(self, word):
        if word in self.across_words:
            words = self.across_words
            starts = self.across_starts
            direction = self.ACROSS
        elif word in self.down_words:
            words = self.down_words
            starts = self.down_starts
            direction = self.DOWN
        else:
            raise ValueError("don't have %s" % word)
        for mystart, myword in zip(starts, words):
            if word == myword:
                return mystart, direction

    def get_coords_of(self, word):
        start, direction = self.get_start_of(word)
        x, y = start
        coords = []
        while x < self.W and y < self.H and self.at(x, y) != '#':
            coords.append( (x,y) )
            if direction == self.ACROSS:
                x += 1
            elif direction == self.DOWN:
                y += 1
        return coords

    def get_crosses_of(self, word):
        crosses = []
        for x,y in self.get_coords_of(word):
            a,d = self.words[(x,y)]
            if a == word:
                crosses.append(d)
            else:
                crosses.append(a)

        assert len(crosses) == len(word)
        return crosses

    def proposed_new_crosses(self, before_word, new_word):
        assert len( before_word ) == len( new_word )

        g = Grid(self.state())
        g.fill(before_word, new_word)
        return g.get_crosses_of(new_word)

    def fill(self, before_word, new_word):
        assert len(before_word) == len(new_word)
        i = 0
        for (x, y) in self.get_coords_of(before_word):
            row = self.G[y]
            self.G[y] = row[:x] + new_word[i] + row[x+1:]
            i += 1
        # refresh
        self.__find_words()

    def state(self):
        return '\n'.join(self.G)

    def is_complete(self):
        for w in self.across_words + self.down_words:
            if '_' in w:
                return False
        return True

    def solve(self, debug=True):
        """Try to "solve" the puzzle"""
        if debug:
            cls()
            print
            print str(self)
        if self.is_complete():
            return self

        # try and fill the hardest remaining slot
        def slot_easiness(s):
            return len(words_that_fit(s))

        remaining_words = sorted([w for w in self.across_words + self.down_words if '_' in w], key=slot_easiness)
        noms = []
        for nom in remaining_words:
            if slot_easiness(nom) == slot_easiness(remaining_words[0]):
                noms.append(nom)
            else:
                break
        nom = random.choice(noms)
        possibles = list(words_that_fit(nom))
        if not possibles:
            # cornered, fall back and pursue other options
            return
        random.shuffle(possibles)
        possibles = possibles[:200]
        def new_score(prop):
            return sum( map(score, self.proposed_new_crosses(nom, prop)) )

        scores = map(new_score, possibles)
        best = sorted( zip(scores, possibles), reverse=True )[:20]
        random.shuffle(best)

        for _, new_word in best:
            if new_word in (self.across_words + self.down_words):
                # don't reuse words
                continue
            # try to put the word in
            g2 = Grid(self.state())
            g2.fill(nom, new_word)
            for new_cross in g2.get_crosses_of(new_word):
                if len(new_cross) == 1:
                    continue
                if not words_that_fit(new_cross):
                    break
            else:
                p = g2.solve()
                if p:
                    return p

        return



    def __str__(self):
        return '\n'.join(self.G)

if __name__ == "__main__":
    setup()
    gridstr = """
##____
#_____
______
____##
___###
"""
    gridstr = """
______#_________
______#_________
______#_________
____#______#____
_____#_____#____
#_________###___
##____##___#____
###__________###
____#___##____##
___###_________#
____#_____#_____
____#______#____
_________#______
_________#______
_________#______
"""
    p = Grid(gridstr)
    print p

    p2 = p.solve()
    print "@@@@@@@@@@@@@@"
    print p2
