import re
import sys
import random

g_dict_file = r'.\txt\18thCdialectdict.txt'

g_outfile = r"C:\tmp\defjam.txt"

g_defines = dict()
g_search_corpus = list()

g_define_re = re.compile(r"""
    ^
    (?P<term>[^\]:]+)
    (?P<extra>.*?)
    \s*
    (?P<def>.*)$
    """, re.VERBOSE | re.MULTILINE
)

def levenshtein_distance(first, second):
    """Find the Levenshtein distance between two strings.
    Taken from http://www.korokithakis.net/node/87"""
    if len(first) > len(second):
        first, second = second, first
    if len(second) == 0:
        return len(first)
    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [[0] * second_length for _ in range(first_length)]
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

def create_define_dict():
    with open(g_dict_file) as df:
        src_txt = df.read()
    for wdef in g_define_re.finditer(src_txt):
        dd = wdef.groupdict()
        term = dd['term']
        extra = dd.get('extra')
        definition = dd.get('def')
        if term not in g_defines:
            g_defines[term] = list()
        if len(extra) > 5:
            continue
        if len(definition) < 5:
            continue
        g_defines[term].append(definition)
        g_search_corpus.append(definition)

def index_by_word(initial_dict):
    """map individual words used in descriptions back to their owning word"""
    word_dict = dict()
    for defined_word in initial_dict.keys():
        for desc in initial_dict[defined_word]:
            for desc_w in desc.split():
                dw = desc_w.lower()
                if dw not in word_dict:
                    word_dict[dw] = []
                word_dict[dw].append(defined_word)
    return word_dict

def find_match(args, word_dict, def_dict):
    for arg in args:
        if arg.lower() in word_dict:
            # random chance to keep looking
            if random.random() < 0.3:
                continue
            associated_def = random.choice(word_dict[arg.lower()])
            #print arg.lower(), "in word dict"
            return associated_def, random.choice(def_dict[associated_def])
    argstr = ' '.join(args)
    distances = map(lambda c: levenshtein_distance(argstr, c), def_dict.keys())
    min_dst = min(distances)
    res = []
    for i, (key, entry) in enumerate(def_dict.items()):
        if distances[i] <= min_dst + 1:
            #print argstr, distances[i], key, entry
            res.append((key, entry))
    defw, entries = random.choice(res)
    return defw, random.choice(entries)

def getstr(args):
    if not g_search_corpus:
        create_define_dict()
    wd = index_by_word(g_defines)
    print "args", args
    retword, retstr = find_match(args, wd, g_defines)
    print repr(retword), repr(retstr)
    return '%s: %s' % (retword, retstr)

def main(args):
    s = getstr(args)
    with open(g_outfile, 'w') as outf:
        outf.write(s)

if __name__ == "__main__":
    main(sys.argv[1:])