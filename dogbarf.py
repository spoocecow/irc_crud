import random
import math, cmath
import inspect
import os, sys
import re
from acrobot import Acro

_thisfile = inspect.getfile(inspect.currentframe())
cwd = os.path.dirname(os.path.abspath(_thisfile))

DOGSOURCE = os.path.join(cwd, "txt", "dogs.txt")

def get_dumdum():
    if random.random() < 0.222:
        return Acro.generate_insult()

    dummies = ['dummy', 'idiot', 'dumdum', 'nincompoop', 'dummo', 'stinkbrain', 'dumbface', 'craphead',
               'jerk', 'ya putz', 'dumbbell', 'loser', 'moron', 'Punky Brewster', 'fuckbarn', 'jabroni']
    return random.choice(dummies)
    
def get_mean_dumdum():
    return random.choice(
        ['fucker', 'scoundrel', 'bastard', 'devil', 'bad person', 'Jerk', 'cad', 'charlatan']
    )

def get_friend():
    return random.choice(
        ['friend', 'pal', 'buddy', 'chum', 'fella', 'my friend', 'fellow dog enthusiast']
    )

def get_pleasantry():
    return random.choice(
        ['Have a nice day', 'Have a great day', 'Cheers', 'Thanks', 'Thank you',
         'Take care', 'Have a good one', "Here's to you", "You look great today"]
    )

def get_unpleasantry():
    return random.choice(
        ["u stink.", "hmmmmm, nah."] * 4 +
        ["no that's bad.", "why u do this to me."] * 2 +
        ["u havin a laugh???", "I do not like your request.", "I can't read :("] * 2 +
        ["what you typed was incomprehensible to little ol' me..."]
    )


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
            retfmt = 'Here {plur} {dognum:.0f} dog{dogplur}, {dummy}:'
            return dognum, retfmt.format(dognum=dognum, dummy=get_friend(), plur=plur, dogplur=dogplur)
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
            'all': 4.20, 'every': 4.20, 'infinite': 4.20, 'infinity': 4.20, 'all the': 4.20,
            'five':5, 'several':5,
            'six':6, 'more':6,
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
            'eighteen':18, 'a ton of':18,
            'nineteen':19,
            'twenty':20}
        operations = {
            'plus': '+', 'add': '+', 'and': '+',
            'minus': '-', 'subtract': '-',
            'times': '*', 'multiply': '*',
            'divided by': '/', 'divide': '/', 'over': '/',
            '^': '**', 'to the power of': '**'}
        if reqnum in eng_2_num:
            if type(eng_2_num[reqnum]) is complex:
                dognum = -1 * eng_2_num[reqnum].imag
                return dognum, "thanks for being difficult {dummy}, here's {dognum} imaginary dogs:".format(dognum=abs(dognum), dummy=get_mean_dumdum())
            dognum = float( eng_2_num[reqnum] )
        else:
            replaced = reqnum[:]
            replacements = []
            for p in operations:
                if p in replaced:
                    replaced = replaced.replace(p, operations[p])
            for p in eng_2_num:
                if ('a '+p) in replaced:
                    print 'plonk', eng_2_num[p]
                    replacements.append( ('a ' + p, eng_2_num[p]) )
                elif p in replaced:
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
            evalstr = replaced
            if any( map(str.isalpha, evalstr) ) or '=' in evalstr:
                print "Invalid/not replaceable, not evaling:", reqnum, " (AKA", evalstr, ')'
                dognum = random.randint(2,7)
                retfmt = '{nothx} Here are {dognum:.0f} dogs, {dummy}:'
                return dognum, retfmt.format(nothx=get_unpleasantry(), dognum=dognum, dummy=get_dumdum())
            else:
                print "evaluating", evalstr
                try:
                    dognum = float( eval(evalstr) )
                    print "dognum = ", dognum
                except (SyntaxError, NameError, ZeroDivisionError):
                    return -1, "u are a {} and a true {}".format( get_mean_dumdum(), get_mean_dumdum() )
                except TypeError:
                    print "Barf!", evalstr
                    dognum = random.randint(2,4)
                    retfmt = "BARF. I can't evaluate `{evalstr}`. So here are {dognum:.0f} dogs, {dummy}:"
                    return dognum, retfmt.format(dognum=dognum, dummy=get_dumdum(), evalstr=evalstr)
                except ValueError:
                    print "waaaahhhh"
                    dognum = random.randint(2,6)
                    retfmt = "FINE. I can't evaluate `{evalstr}`. So here are {dognum:.0f} dogs, {dummy}:"
                    return dognum, retfmt.format(dognum=dognum, dummy=get_dumdum(), evalstr=evalstr)
    if dognum == 1:
        plur = 'is'
        dogplur = ''
    if dognum % 1 != 0:
            retfmt = 'Here {plur} {dognum:.2f} dog{dogplur}:'
    return dognum, retfmt.format(dognum=dognum, plur=plur, dogplur=dogplur)

def get_some_dogs(num=1):
    with open(DOGSOURCE) as dogf:
        dogs = dogf.readlines()
    dog_selections = random.sample( xrange(len(dogs)), num )
    for dog_choice in dog_selections:
        yield dogs[dog_choice].strip()

def dogsay(arg):
    import string
    arg = filter(lambda c: c in string.printable, arg)
    re_arg = re.search(r"\s*(.+?)\s+dog", arg)
    if re_arg:
        print "blao"
        new_arg = re_arg.group(1)
    else:
        # taking a guess
        new_arg = arg.replace('dogs', '').replace('dog', '').strip()
    print "arg=", new_arg
    dognum, prefix = get_dog_fmt(new_arg)
    formatter = lambda c: c
    if dognum < 0 and 'u are a' in prefix:
        return prefix + " >:(!!!!"  # we are very cross now
    elif dognum < 0:
        formatter = lambda c: ''.join((reversed(c)))
        dognum = abs(dognum)
    if dognum == 0 or dognum > 20:
        if random.random() < 0.33:
            return get_unpleasantry() + ' NO DOGS FOR U >:('
        else:
            return 'You are a ' + get_dumdum() + ' and u get NO DOGS >:('

    dog_getter = get_some_dogs(int(dognum))
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
    if 'please' in arg.lower():
        s += ' %s, %s!' % (get_pleasantry(), get_friend())
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