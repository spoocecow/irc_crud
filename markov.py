#!/bin/python
# Really simple Markov chain-based text generator.
import sys, random

N = 4
STOP = "\n"
table = {}

def levenshtein_distance(first, second):
    """Find the Levenshtein distance between two strings.
    Taken from http://www.korokithakis.net/node/87"""
    if len(first) > len(second):
        first, second = second, first
    if len(second) == 0:
        return len(first)
    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [[0] * second_length for x in range(first_length)]
    for i in range(first_length):
       distance_matrix[i][0] = i
    for j in range(second_length):
       distance_matrix[0][j]=j
    for i in xrange(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i-1][j] + 1
            insertion = distance_matrix[i][j-1] + 1
            substitution = distance_matrix[i-1][j-1]
            if first[i-1] != second[j-1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)
    return distance_matrix[first_length-1][second_length-1]

class Record(object):
    def __init__(self, start):
        self.start = start # ex. 'qua'
        self.__hash = hash(start.lower())
        self.count = 1
        self.goto = {} # ex. 'qua'.goto = { 'ck ': 3, 'rk ': 2, 'int': 1 }

    def add(self, entry):
        if entry not in self.goto:
            self.goto[entry] = 0
        self.goto[entry] += 1
        self.count += 1
            
    def build(self, hint=None):
        if self.start == STOP:
            return self.start
        n = self.pick()
        if not n:
            return self.start
        else:
            return self.start + " " + n.build()

    def next(self, hint=None):
        if not hint:
            return self.pick( self.start )

        if hint in self.goto:
            return self.pick(hint)
        else:
            distances = map( lambda x: (levenshtein_distance(hint,x),x) ,\
                             self.goto.keys() )
            # ex. [(1,'ck '), (2, 'rk '), (3, 'int')]
            return pick( min(distances)[1] )

    def pick(self, e_text=None):
        if not e_text:
            e_text = self.start
        entry = table[e_text]
        t = entry.count
        n = random.uniform(0, t)
        for txt in entry.goto:
            count = entry.goto[txt]
            if n < count:
                return txt
            n = n - count
        return None

    def __hash__(self):
        return self.__hash

    def __str__(self):
        return "record("+self.start+")"
        

def read_file(filename):
    f = open(filename, 'r')
    if not f:
        return None
    text = f.read()
    text = text.replace("\n"," ")
    text = text.replace("\f", " ")
    text = text.replace("\r", " ")
    text = text.split()
    word = None

    for follow in text:
        if follow not in table:
            table[follow] = Record(follow)
        if word:
            table[word].add( table[follow] )
        word = follow
        
    """
    i = 0
    base = text[i:i+N]
    while i+N < len(text):
        if base not in table:
            table[base] = Record(base)
        follow = text[i+N:i+N+N]
        if follow not in table:
            table[follow] = Record(follow)
        table[base].add( table[follow] )
        i += 1
        base = text[i:i+N]
    """

def read_log(filename, mynick):
    f = open(filename, 'r')
    if not f:
        return None
    log = f.readlines()
    text = []
    for line in log:
        line = line.strip()
        if mynick in line:
            continue
        nick,junk,l = line.partition(">")
        if l and not nick.endswith(mynick):
            text.extend(l.split())
            text.append("\n")
    word = None
    for follow in text:
        if follow not in table:
            table[follow] = Record(follow)
        if word:
            table[word].add( table[follow] )
        word = follow

def add_line(line):
    line = line.strip()
    line = line.split()
    word = None
    for follow in line:
        if follow not in table:
            table[follow] = Record(follow)
        if word:
            table[word].add( table[follow] )
        word = follow

def talk(hint=None, l=100):
    if not hint:
        start = random.choice(table.values())
    elif hint not in table:
        least = 1000
        leastW = random.choice(table.keys())
        print "random key:",leastW
        for w in hint.split():
            if w in table:
                leastW = w
                break
            for i in xrange(l):
                start = random.choice(table.keys())
                d = levenshtein_distance(hint, start)
                if d < least:
                    least = d
                    leastW = start
        start = table[leastW]
    else:
        start = table[hint]
    print "start = <%s>" % start
    s = start.build()
    i = 0
    while len(s) < l:
        s = start.build()
        i += 1
        if i > l:
            return None
    return s

def main(argv):

    for arg in argv:
        read_file(arg)

    for i in range(20):
        start = random.choice(table.values())
        print start.build()
        print "-------------"


if __name__ == "__main__":
    main(sys.argv[1:])
