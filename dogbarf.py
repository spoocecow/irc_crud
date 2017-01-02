from __future__ import division
import random
import math, cmath
import inspect
import os, sys
import re
from acrobot import Acro

_thisfile = inspect.getfile(inspect.currentframe())
cwd = os.path.dirname(os.path.abspath(_thisfile))

DOGSOURCE = os.path.join(cwd, "txt", "dogs.txt")
GODSOURCE = os.path.join(cwd, "txt", "gods.tsv")
g_includeReligions = False


class ZERODOGSRESPONSE(object):
    pass

def get_dumdum():
    if random.random() < 0.35:
        return Acro.generate_insult()

    dummies = ['dummy', 'idiot', 'dumdum', 'nincompoop', 'dummo', 'stinkbrain', 'dumbface', 'craphead', 'nerd',
               'jerk', 'ya putz', 'dumbbell', 'loser', 'moron', 'Punky Brewster', 'fuckbarn', 'jabroni']
    return random.choice(dummies)
    
def get_mean_dumdum():
    return random.choice(
        ['fucker', 'scoundrel', 'bastard', 'devil', 'bad person', 'Jerk', 'cad', 'charlatan', 'roustabout', 'nerd', "ne'erdowell", 'scamp']
    )

def get_friend():
    return random.choice(
        ['friend', 'pal', 'buddy', 'chum', 'fella', 'my friend', 'my good fellow'] * 2 +
        ['fellow dog enthusiast', 'champ', 'tiger', 'chief', 'you good good dog boy']
    )

def get_pleasantry():
    return random.choice(
        ['Have a nice day', 'Have a great day', 'Cheers', 'Thanks', 'Thank you',
         'Take care', 'Have a good one', "Here's to you", "You look great today"]
    )

def get_unpleasantry():
    return random.choice(
        ["u stink.", "hmmmmm, nah."] * 3 +
        ["no that's bad.", "why u do this to me."] * 2 +
        ["u havin a laugh???", "I do not like your request.", "I can't read :("] +
        ["this is simply unacceptable.", "why i oughta......."] +
        ["no! no! this will not do at all!"] + 
        ["what you typed was incomprehensible to little ol' me..."]
    )

def check_evalstr(evalstr):
    badlist = (
        'os.',
        'sys.',
        'inspect.',
        're.',
        'lambda',
        'input',
    )
    for badword in badlist:
        if badword in evalstr:
            return False
    return True

def get_dog_fmt(reqnum):
    print repr(reqnum)
    plur = 'are'
    dogplur = 's'
    retfmt = 'Here {plur} {dognum:.0f} dog{dogplur}:'
    try:
        dognum = float(reqnum)
    except ValueError:
        easy_cases = {'a':1, 'an':1, 'the':1, '':0, 'NaN': 0, 'nan':0, 'NAN':0}
        if reqnum in easy_cases:
            dognum = float(easy_cases[reqnum])
            if dognum == 1:
                plur = 'is'
                dogplur = ''
            retfmt = 'Here {plur} {dognum:.0f} dog{dogplur}, {friend}:'
            return dognum, retfmt.format(dognum=dognum, friend=get_friend(), plur=plur, dogplur=dogplur)
        eng_2_num = {
            'e^i*pi': -1, 'e^pi*i': -1, 'e^(i*pi)': -1, 'e^(pi*i)': -1, 'e**i*pi': -1, 'e**pi*i':-1, 'e**(i*pi)': -1, 'e**(pi*i)': -1,
            'i': cmath.sqrt(-1),
            'zero': 0, 'no': 0, 'none':0,
            'tenth': 0.1,
            'ninth': 1.0/9,
            'eighth': 1.0/8,
            'seventh': 1.0/7,
            'sixth': 1.0/6,
            'fifth': 1.0/5,
            'fourth': 1.0/4, 'quarter': 1.0/4,
            'third': 1.0/3,
            'half': 0.5, 'a half': 0.5, 'one half': 0.5, 'half a': 0.5, 'half of a': 0.5,
            'one':1, 'just one':1, 'a single':1, #' a ': 1, 'the': 1,
            'two':2, 'a couple':2, 'a couple of':2,
            'not many': 2.5,
            'e': math.e,
            'three':3, 'a few':3,
            'pi': math.pi,
            'four':4, 'some':4,
            'all': 4.20, 'every': 4.20, 'infinite': 4.20, 'infinity': 4.20, 'all the': 4.20, 'maximum': 4.20,
            'five':5, 'several':5,
            'six':6, 'more':6,
            'a nice amount of': 6.90, 'a good amount of': 6.90,
            'seven':7,
            'eight':8, 'a bunch':8, 'a bunch of':8, 'a buncha':8,
            'nine':9, 'a cluster of':9,
            'ten':10,
            'eleven':11, 'a lot':11, 'a lot of':11, 'a lotta':11, 'lotsa':11,
            'twelve':12, 'a dozen':12, 'one dozen':12,
            'thirteen':13, 'bakers dozen':13, 'a bakers dozen': 13, 'a bakers dozen of':13, "a baker's dozen of":13, "a bakers dozen of":13,
            'fourteen':14, 'many': 14,
            'fifteen':15, 'plenty of':15,
            'sixteen':16, 'too many':16,
            'seventeen':17,
            'eighteen':18, 'a ton of':18, 'tons of':18,
            'nineteen':19,
            'twenty':20}
        operations = {
            'plus': '+', 'add': '+', 'and': '+',
            'minus': '-', 'subtract': '-',
            'times': '*', 'multiply': '*',
            'divided by': '/', 'divide': '/', 'over': '/',
            '^': '**', 'to the power of': '**',
            'squared': '**2', 'cubed': '**3',
        }
        if reqnum in eng_2_num:
            if type(eng_2_num[reqnum]) is complex:
                dognum = -1 * eng_2_num[reqnum].imag
                return dognum, "thanks for being difficult {dummy}, here's {dognum} imaginary dogs:".format(dognum=abs(dognum), dummy=get_dumdum())
            dognum = float( eng_2_num[reqnum] )
        else:
            replaced = reqnum.lower()
            replacements = []
            for p in operations:
                if p in replaced:
                    replaced = replaced.replace(p, operations[p])
            for p in eng_2_num:
                if ('a '+p) in replaced:
                    print 'plonk', eng_2_num[p]
                    replacements.append( ('a ' + p, eng_2_num[p]) )
                elif re.search(r'\W' + re.escape(p), replaced):
                    print 'glonk', p, eng_2_num[p]
                    replacements.append( (p, eng_2_num[p]) )
            available_reps = replacements[:]
            for rep1 in replacements:
                p1, r1 = rep1
                for rep2 in replacements:
                    p2, r2 = rep2
                    if p1 == p2:
                        continue
                    elif p2 in p1:
                        # keep only the largest match
                        if rep2 in available_reps:
                            available_reps.remove(rep2)
            for final_rep in available_reps:
                p, rep = final_rep
                replaced = replaced.replace(p, str(rep))
            # also do some massaging for math notation that doesn't eval like one might expect
            replaced = re.sub(r'(\d+)!', r'math.factorial(\1)', replaced)
            evalstr = replaced
            if not check_evalstr(evalstr):
                print "Invalid/not replaceable, not evaling:", reqnum, " (AKA", evalstr, ')'
                dognum = random.uniform(2,6)
                retfmt = 'Nice try {dingdong}!!!!! Here are {dognum:.0f} dogs, {dummy}:'
                return dognum, retfmt.format(dingdong=get_friend(), dognum=dognum, dummy=get_mean_dumdum())
            else:
                print "evaluating", evalstr
                rv = None
                try:
                    rv = eval(evalstr)
                    dognum = float( rv )
                    print "dognum = ", dognum
                except (SyntaxError, NameError, ZeroDivisionError, OverflowError):
                    return -1, "u are a {} and a true {}".format( get_dumdum(), get_mean_dumdum() )
                except TypeError:
                    print "Barf!", evalstr
                    if type(rv) is complex:
                        # to flatten to int... idk, get magnitude as polar coord.
                        dognum = ((rv.real**2) + (rv.imag**2))**0.5
                        return dognum, "thanks for being difficult {dummy}, here's {dognum} complex dogs:".format(dognum=dognum, dummy=get_dumdum())
                    dognum = random.randint(2,4)
                    retfmt = "BARF. I can't evaluate `{evalstr}`. So here are {dognum:.0f} dogs, {dummy}:"
                    return dognum, retfmt.format(dognum=dognum, dummy=get_dumdum(), evalstr=evalstr)
                except ValueError:
                    print "waaaahhhh"
                    dognum = random.randint(2,6)
                    retfmt = "FINE. I can't evaluate `{evalstr}`. So here are {dognum:.0f} dogs, {dummy}:"
                    return dognum, retfmt.format(dognum=dognum, dummy=get_mean_dumdum(), evalstr=evalstr)
    if dognum == 1:
        plur = 'is'
        dogplur = ''
    elif dognum == 0:
        existential_questions = (
            'Why did you want no dogs?',
            'No dogs? Why?',
            'No dogs? At all? Why?',
            'Why must you try me so? I am a humble script and handling zero is hard for me.',
            "I don't know why you want this. Here are no dogs.",
            'I exist to serve dogs. Please request some dogs, or leave me in peace.',
            "I don't mean to be rude, but I truly do not understand why you are asking for exactly zero dogs.",
            "No dogs... this request is a mystery to me. In my humble opinion, you should ask for some dogs.",
            "Perhaps there truly is evil in the world. Why would you ask, specifically, for no dogs?",
            "Here are zero dogs. ---->                                <---  I hope you are happy.",
            "No dogs? For you, my friend, I will fulfill this request.",
            "No dogs? For you, sir or madam, I will gladly fulfill this request.",
            "No dogs? For you, stranger, I will grudgingly fulfill this request.",
        )
        return ZERODOGSRESPONSE(), random.choice(existential_questions)
    elif dognum % 1 != 0:
        retfmt = 'Here {plur} {dognum:.2f} dog{dogplur}:'
    return dognum, retfmt.format(dognum=dognum, plur=plur, dogplur=dogplur)

def get_some_dogs(num=1):
    with open(DOGSOURCE) as dogf:
        dogs = dogf.readlines()
    dog_selections = random.sample( xrange(len(dogs)), num )
    for dog_choice in dog_selections:
        yield dogs[dog_choice].strip()

def get_some_gods(num=1):
    import codecs
    with codecs.open(GODSOURCE, 'r', 'utf-8') as godf:
        gods = godf.readlines()
    god_selections = random.sample( gods, num )

    naive_str = u'\n'.join(god_selections)
    naive_strlen = len(naive_str)
    rels = list()
    names = list()
    infos = list()
    for m in re.finditer(r"^([^\t]+?)\t([^\t\n]+)\t?(.*)$", naive_str, re.MULTILINE):
        rels.append( m.group(1).strip() )
        names.append( m.group(2).strip() )
        infos.append( m.group(3).strip() )

    info_len = sum(map(len, infos))
    no_rels_strlen = sum(map(len, names + infos))
    if g_includeReligions:
        limit_strlen = naive_strlen
        basic_len = sum(map(len, rels + names))
    else:
        limit_strlen = no_rels_strlen
        basic_len = sum(map(len, names))
    be_concise = (num > 4 and info_len > 300) or (limit_strlen >= 400)  # 510 is irc max limit
    allowed_info_c = 460 - (num * 7) - basic_len  # *7 for bold/ital chrs, etc.

    for religion, god_name, extra_info in zip(rels, names, infos):
        if be_concise:
            room_for_info = 1.0 - (len(extra_info) / abs(allowed_info_c))
        else:
            room_for_info = (allowed_info_c - len(extra_info)) / allowed_info_c

        if random.random() < room_for_info:
            yield religion, god_name, extra_info
            allowed_info_c -= len(extra_info)
        else:
            yield religion, god_name, ''
    return

def make_godstring(arg):
    religion, god, info = arg
    if g_includeReligions:
        retstr = u"{godname}".format( godname=god )
    else:
        retstr = u"{godname}".format(godname=god)

    if info:
        retstr += u' - {info}'.format(info=info)

    if g_includeReligions:
        retstr += u' ({religion})'.format(religion=religion)
    return retstr

def dogsay(arg):
    global g_includeReligions
    import string
    godmode = False
    arg = filter(lambda c: c in string.printable, arg)
    re_arg = re.search(r"\s*(.+?)\s+(dog|god)", arg)
    if re_arg:
        new_arg = re_arg.group(1)
        if re_arg.group(2) == 'god':
            godmode = True
    else:
        # taking a guess
        new_arg = arg.replace('dogs', '').replace('dog', '').strip()
    print "arg=", new_arg
    dognum, prefix = get_dog_fmt(new_arg)

    politeness_enabled = 'please' in arg.lower()
    g_includeReligions |= politeness_enabled
    polite_tag = ' %s, %s!' % (get_pleasantry( ), get_friend( ))

    base_formatter = lambda c: c
    if godmode:
        prefix = prefix.replace('dog', 'god')
        polite_tag = polite_tag.replace('dog', 'god')
        base_formatter = make_godstring
    formatter = base_formatter

    if dognum < 0 and 'u are a' in prefix:
        if politeness_enabled:
            return prefix + ", " + get_friend() + "!!!!"
        else:
            return prefix + " >:(!!!!"  # we are very cross now
    elif dognum < 0:
        formatter = lambda c: ''.join((reversed(base_formatter(c))))
        dognum = abs(dognum)
    elif isinstance(dognum, ZERODOGSRESPONSE):
        # someone is being a real piece of work!!
        if politeness_enabled:
            prefix += ' %s, %s!' % (get_pleasantry(), get_friend())
        return prefix
    if dognum == 0 or dognum > 20:
        things = 'GODS' if godmode else 'DOGS'
        face = ':/' if politeness_enabled else '>:('
        spin = random.random()
        if politeness_enabled: spin -= 0.12345  # make polite option below more likely
        if spin < 0.0271828:
            return 'u should reconsider your behavior... i know you can do better, {guy}'.format(guy=get_friend())
        elif spin < 0.55:
            return '{nope} NO {thing} FOR U {face}'.format(nope=get_unpleasantry(), thing=things, face=face)
        elif spin < 0.6:
            return '{nope} THERE WILL BE NO {thing} FOR {jerk}S LIKE U {face}'.format(nope=get_unpleasantry().upper(), jerk=get_dumdum().upper(), thing=things, face=face)
        else:
            return 'You are a {jerk} and u get NO {things} {face}'.format(jerk=get_dumdum(), things=things, face=face)

    if godmode:
        dog_getter = get_some_gods(int(math.ceil(dognum)))
        get_dog = dog_getter.next
    else:
        dog_getter = get_some_dogs(int(math.ceil(dognum)))
        get_dog = dog_getter.next

    s = prefix + ' '
    i = dognum
    while i > 1:
        s += formatter(get_dog()) + ', '
        i -= 1
    if dognum <= 2:
        s = s.replace(',', '')
    if dognum > 1:
        s += 'and '
    last_dog = formatter(get_dog())
    if i == 1:
        s += last_dog + '.'
    else:
        d_pct = int(i * len(last_dog))
        rev_chr = ''
        s += last_dog[:d_pct] + rev_chr + last_dog[d_pct:] + rev_chr + '.'
    if politeness_enabled:
        s += polite_tag
    return s

def serve_dogbarf(arg):
    data = dogsay(arg)
    if not data:
        return False
    dogbarf_file = r'C:\tmp\dogbarf.txt'
    if os.path.exists(dogbarf_file):
        os.unlink(dogbarf_file)
    if not os.path.exists(r'C:\tmp'):
        os.makedirs(r'C:\tmp')
    with open(dogbarf_file, 'w+') as dogf:
        dogf.write(data.rstrip())
    return True

if __name__ == "__main__":
    serve_dogbarf(' '.join(sys.argv[1:]))