import os
import random
import sys
import time

def cls():
    #print('\033[H\033[J')
    os.system('clear')


g_letters = 'abcdefghijklmnopqrstuvwxyz'
g_corp = []

L = {l: [] for l in g_letters}  # words indexed by letter/space
M = {l: [] for l in g_letters}  # probability of letter at space
W = dict()  # words indexed by length

def setup():
    global g_corp
    global L
    global M
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

    for letter in L:
        places = L[letter]
        all_places = sum(map(len, places))
        M[letter] = [0] * len(places)
        for i, p in enumerate(places):
            M[letter][i] = len(places[i]) / float(all_places)

    print time.time() - t, sys.getsizeof(L)

def words_with_letter(letter, place):
    return set(L[letter][place])

def words_that_fit(template, match_length=True):
    # special case: no letters filled in at all
    if template == '_' * len(template):
        return W[len(template)]

    rv = []
    for i, letter in enumerate(template):
        if letter not in g_letters:
            continue
        s = words_with_letter(letter, i)
        if match_length:
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

class Grid(object):

    ACROSS = 0
    DOWN = 1

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
        for across_start in self.across_starts:
            x, y = across_start
            w = ''
            coords = []
            while x < self.W and self.at(x, y) != '#':
                w += self.at(x,y)
                coords.append( (x,y) )
                x += 1
            self.across_words.append(w)
            self.across_coords.append(coords)
        for down_start in self.down_starts:
            x, y = down_start
            w = ''
            coords = []
            while y < self.H and self.at(x, y) != '#':
                w += self.at(x, y)
                coords.append( (x, y) )
                y += 1
            self.down_words.append(w)
            self.down_coords.append(coords)

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
        start, direction = self.get_start_of(word)
        if direction == self.ACROSS:
            possibles = self.down_coords
            ref_words = self.down_words
        else:
            possibles = self.across_coords
            ref_words = self.across_words
        for x,y in self.get_coords_of(word):
            for i, nom in enumerate(possibles):
                if (x,y) in nom:
                    crosses.append(ref_words[i])
                    break
        assert len(crosses) == len(word)
        return crosses

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
            print str(self)
        if self.is_complete():
            print "8)"
            return self
        # try and fill the longest remaining word
        remaining_words = sorted([w for w in self.across_words + self.down_words if '_' in w], key=len, reverse=True)
        nom = remaining_words[0]
        possibles = list(words_that_fit(nom))
        if not possibles:
            # cornered, fall back and pursue other options
            # if debug:
            #     print "WAH"
            return
        random.shuffle(possibles)
        for new_word in possibles[:20]:
            # try to put the word in
            g2 = Grid(self.state())
            g2.fill(nom, new_word)
            for new_cross in g2.get_crosses_of(new_word):
                if '_' in new_cross:
                    continue
                if new_cross not in g_corp:
                    break
            else:
                p = g2.solve()
                if p:
                    return p
        #     else:
        #         print "wah"
        # print "wwwwfggggg"
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
    p = Grid(gridstr)
    print p

    p2 = p.solve()
    print "@@@@@@@@@@@@@@"
    print p2
