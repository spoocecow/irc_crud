# coding=utf-8
from __future__ import division
import codecs
import math, cmath
import inspect
import json
import os, sys
import random
import re
import zipfile
from acrobot import Acro

_thisfile = inspect.getfile( inspect.currentframe() )
cwd = os.path.dirname( os.path.abspath( _thisfile ) )
# https://github.com/dariusk/corpora
corpora_wd = os.path.join(cwd, '..', 'corpora', 'data')

g_verbose = False


class ZEROTHINGSRESPONSE( object ):
    pass


def get_dumdum():
    if random.random() < 0.35:
        return Acro.generate_insult()

    dummies = ['dummy', 'idiot', 'dumdum', 'nincompoop', 'dummo', 'stinkbrain', 'dumbface', 'craphead', 'nerd',
               'jerk', 'ya putz', 'dumbbell', 'loser', 'moron', 'Punky Brewster', 'fuckbarn', 'jabroni']
    return random.choice( dummies )


def get_mean_dumdum():
    return random.choice(
        ['fucker', 'scoundrel', 'bastard', 'devil', 'bad person', 'Jerk', 'cad', 'charlatan', 'roustabout', 'nerd',
         "ne'erdowell", 'scamp']
    )


def get_friend():
    return random.choice(
        ['friend', 'pal', 'buddy', 'chum', 'fella', 'my friend', 'my good fellow'] * 2 +
        ['fellow {thing} enthusiast', 'champ', 'tiger', 'chief', 'you good good {thing} boy']
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


def get_thing_overflow_exception(things):
    return random.choice(
        ["that's too many {things}", "Too many {things}!", "Way too many {things}!"] * 2 +
        ["That's too much! You're too greedy for {things}!",
         "ALERT: {things} overflow exception. ur in trouble bud.",
         "oh my gosh that's so many {things}. cool it, hombre.",
         "That's too many {things} and you KNOW it. For shame.",
         "cool it with all the {things}... yikes."]
    ).format( things=things )


def get_no_things_existential_crisis():
    existential_questions = (
        'Why did you want no {things}?',
        'No {things}? Why?',
        'No {things}? At all? Why?',
        'Why must you try me so? I am a humble script and handling zero is hard for me.',
        "I don't know why you want this. Here are no {things}.",
        'I exist to serve {things}. Please request some {things}, or leave me in peace.',
        "I don't mean to be rude, but I truly do not understand why you are asking for exactly zero {things}.",
        "No {things}... this request is a mystery to me. In my humble opinion, you should ask for some {things}.",
        "Perhaps there truly is evil in the world. Why would you ask, specifically, for no {things}?",
        "Here are zero {things}. ---->                                <---  I hope you are happy.",
        "No {things}? For you, my friend, I will fulfill this request.",
        "No {things}? For you, sir or madam, I will gladly fulfill this request.",
        "No {things}? For you, stranger, I will grudgingly fulfill this request.",
    )
    return random.choice(existential_questions)

def check_evalstr(evalstr):
    badlist = (
        'os.',
        'sys.',
        'inspect.',
        're.',
        #'lambda',
        'input',
        'exit',
    )
    for badword in badlist:
        if badword in evalstr:
            return False
    return True


def get_thing_fmt(reqnum):
    print repr( reqnum )
    plur = 'are'
    retfmt = 'Here {plur} {thingnum:.0f} {{things}}:'
    try:
        thingnum = float( reqnum )
    except ValueError:
        easy_cases = {'a': 1, 'an': 1, 'the': 1, '': 0, 'NaN': 0, 'nan': 0, 'NAN': 0}
        if reqnum in easy_cases:
            thingnum = float( easy_cases[reqnum] )
            if thingnum == 1:
                plur = 'is'
            retfmt = 'Here {plur} {thingnum:.0f} {{things}}, {friend}:'
            return thingnum, retfmt.format( thingnum=thingnum, friend=get_friend(), plur=plur )
        if reqnum.lower() in ('im', "i'm", "i am"):
            if random.random() < 0.13:
                return ZEROTHINGSRESPONSE(), random.choice(
                    ["no I'M {{thing}}s", "No, **I'M** {{things}}", "no... i'm {{things}}"] ) + random.choice( ['', '.'] )
            return ZEROTHINGSRESPONSE(), '{ok} {ur} {{things}}.'.format(
                ok=random.choice( ['', 'OK,', 'ok,', 'ok', 'ok...', 'ya,', 'Yes,', 'k', 'k...', 'k.'] ),
                ur=random.choice( ['ur', 'ur', 'ur', 'you are', 'your', "you're", 'u r', "u're", "you ARE"] )
            ).strip()

        eng_2_num = {
            'e^i*pi': -1, 'e^pi*i': -1, 'e^(i*pi)': -1, 'e^(pi*i)': -1, 'e**i*pi': -1, 'e**pi*i': -1, 'e**(i*pi)': -1,
            'e**(pi*i)': -1,
            'i': cmath.sqrt( -1 ),
            'zero': 0, 'no': 0, 'none': 0,
            'tenth': 0.1,
            'ninth': 1.0 / 9,
            'eighth': 1.0 / 8,
            'seventh': 1.0 / 7,
            'sixth': 1.0 / 6,
            'fifth': 1.0 / 5,
            'fourth': 1.0 / 4, 'quarter': 1.0 / 4,
            'third': 1.0 / 3,
            'half': 0.5, 'a half': 0.5, 'one half': 0.5, 'half a': 0.5, 'half of a': 0.5,
            'one': 1, 'just one': 1, 'a single': 1,  # ' a ': 1, 'the': 1,
            'two': 2, 'a couple': 2, 'a couple of': 2,
            'not many': 2.5,
            'e': math.e,
            'three': 3, 'a few': 3,
            'pi': math.pi, 'π': math.pi,
            'four': 4, 'some': 4,
            'all': 4.20, 'every': 4.20, 'infinite': 4.20, 'infinity': 4.20, 'all the': 4.20, 'maximum': 4.20,
            'five': 5, 'several': 5,
            'six': 6, 'more': 6,
            'a nice amount of': 6.90, 'a good amount of': 6.90,
            'a nice number of': 6.90, 'a good number of': 6.90,
            'seven': 7,
            'eight': 8, 'a bunch': 8, 'a bunch of': 8, 'a buncha': 8,
            'nine': 9, 'a cluster of': 9,
            'ten': 10,
            'eleven': 11, 'a lot': 11, 'a lot of': 11, 'a lotta': 11, 'lotsa': 11,
            'twelve': 12, 'a dozen': 12, 'one dozen': 12,
            'thirteen': 13, 'bakers dozen': 13, 'a bakers dozen': 13, 'a bakers dozen of': 13, "a baker's dozen of": 13,
            "a bakers dozen of": 13,
            'fourteen': 14, 'many': 14,
            'fifteen': 15, 'plenty of': 15,
            'sixteen': 16, 'too many': 16,
            'seventeen': 17,
            'eighteen': 18, 'a ton of': 18, 'tons of': 18,
            'nineteen': 19,
            'twenty': 20, 'all the': 20}
        operations = {
            'plus': '+', 'add': '+', 'and': '+',
            'minus': '-', 'subtract': '-',
            'times': '*', 'multiply': '*',
            'divided by': '/', 'divide': '/', 'over': '/',
            '^': '**', 'to the power of': '**',
            'squared': '**2', '²': '**2',
            'cubed': '**3', '³': '**3'
        }
        if reqnum in eng_2_num:
            if type( eng_2_num[reqnum] ) is complex:
                thingnum = -1 * eng_2_num[reqnum].imag
                return thingnum, "thanks for being difficult {dummy}, here's {thingnum} imaginary {{things}}:".format(
                    thingnum=abs( thingnum ), dummy=get_dumdum() )
            thingnum = float( eng_2_num[reqnum] )
        else:
            replaced = reqnum.lower()
            replacements = []
            for p in operations:
                if p in replaced:
                    replaced = replaced.replace( p, operations[p] )
            for p in eng_2_num:
                if ('a ' + p) in replaced:
                    print 'plonk', eng_2_num[p]
                    replacements.append( ('a ' + p, eng_2_num[p]) )
                elif re.search( r'(?:^|\W)' + re.escape( p ), replaced ):
                    print 'glonk', p, eng_2_num[p]
                    for match in re.finditer( r'(^|\W)' + re.escape( p ), replaced ):
                        orig_chr = match.group( 1 )
                        replacements.append( (orig_chr + p, orig_chr + str( eng_2_num[p] )) )
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
                            available_reps.remove( rep2 )
            for final_rep in available_reps:
                p, rep = final_rep
                replaced = replaced.replace( p, str( rep ) )
            # also do some massaging for math notation that doesn't eval like one might expect
            replaced = re.sub( r'(\d+)!', r'math.factorial(\1)', replaced )
            evalstr = replaced
            if not check_evalstr( evalstr ):
                print "Invalid/not replaceable, not evaling:", reqnum, " (AKA", evalstr, ')'
                thingnum = random.uniform( 2, 6 )
                retfmt = 'Nice try {dingdong}!!!!! Here are {thingnum:.0f} {{things}}, {dummy}:'
                return thingnum, retfmt.format( dingdong=get_friend(), thingnum=thingnum, dummy=get_mean_dumdum() )
            else:
                print "evaluating", evalstr
                rv = None
                try:
                    rv = eval( evalstr )
                    thingnum = float( rv )
                    print "thingnum = ", thingnum
                except (SyntaxError, NameError, ZeroDivisionError, OverflowError):
                    return -1, "u are a {} and a true {}".format( get_dumdum(), get_mean_dumdum() )
                except TypeError:
                    print "Barf!", evalstr
                    if type( rv ) is complex:
                        # to flatten to int... idk, get magnitude as polar coord.
                        thingnum = ((rv.real ** 2) + (rv.imag ** 2)) ** 0.5
                        return thingnum, "thanks for being difficult {dummy}, here's {thingnum} complex {{things}}:".format(
                            thingnum=thingnum, dummy=get_dumdum() )
                    thingnum = random.randint( 2, 4 )
                    retfmt = "BARF. I can't evaluate `{evalstr}`. So here are {thingnum:.0f} {{things}}, {dummy}:"
                    return thingnum, retfmt.format( thingnum=thingnum, dummy=get_dumdum(), evalstr=evalstr )
                except ValueError:
                    print "waaaahhhh"
                    thingnum = random.randint( 2, 6 )
                    retfmt = "FINE. I can't evaluate `{evalstr}`. So here are {thingnum:.0f} {{things}}, {dummy}:"
                    return thingnum, retfmt.format( thingnum=thingnum, dummy=get_mean_dumdum(), evalstr=evalstr )
    if thingnum == 1:
        plur = 'is'
    elif thingnum == 0:
        return ZEROTHINGSRESPONSE(), get_no_things_existential_crisis()
    elif thingnum % 1 != 0:
        retfmt = 'Here {plur} {thingnum:.2f} {{things}}:'
    return thingnum, retfmt.format( thingnum=thingnum, plur=plur )


def get_some_dogs(num=1):
    with open( os.path.join(cwd, "txt", "dogs.txt") ) as dogf:
        dogs = dogf.readlines()
    dog_selections = random.sample( xrange( len( dogs ) ), num )
    if g_verbose:
        dognames = list(get_simple_json(path=os.path.join(corpora_wd, 'animals', 'dog_names.json'), entry='dog_names'))
    else:
        dognames = []
    for dog_choice in dog_selections:
        if g_verbose:
            yield '{name} the {breed}'.format(name=random.choice(dognames), breed=dogs[dog_choice].strip())
        else:
            yield dogs[dog_choice].strip()


def make_godstring(religion='', god='', info=''):
    if g_verbose:
        retstr = u"{godname}".format( godname=god )
    else:
        retstr = u"{godname}".format( godname=god )

    if info:
        retstr += u' - {info}'.format( info=info )

    if g_verbose:
        retstr += u' ({religion})'.format( religion=religion )
    return retstr


def get_some_gods(num=1):
    with codecs.open( os.path.join(cwd, "txt", "gods.tsv"), 'r', 'utf-8' ) as godf:
        gods = godf.readlines()
    god_selections = random.sample( gods, num )

    naive_str = u'\n'.join( god_selections )
    naive_strlen = len( naive_str )
    rels = list()
    names = list()
    infos = list()
    for m in re.finditer( r"^([^\t]+?)\t([^\t\n]+)\t?(.*)$", naive_str, re.MULTILINE ):
        rels.append( m.group( 1 ).strip() )
        names.append( m.group( 2 ).strip() )
        infos.append( m.group( 3 ).strip() )

    info_len = sum( map( len, infos ) )
    no_rels_strlen = sum( map( len, names + infos ) )
    if g_verbose:
        limit_strlen = naive_strlen
        basic_len = sum( map( len, rels + names ) )
    else:
        limit_strlen = no_rels_strlen
        basic_len = sum( map( len, names ) )
    be_concise = (num > 4 and info_len > 300) or (limit_strlen >= 400)  # 510 is irc max limit
    allowed_info_c = 460 - (num * 7) - basic_len  # *7 for bold/ital chrs, etc.

    for religion, god_name, extra_info in zip( rels, names, infos ):
        if be_concise:
            room_for_info = 1.0 - (len( extra_info ) / abs( allowed_info_c ))
        else:
            room_for_info = (allowed_info_c - len( extra_info )) / allowed_info_c

        if random.random() < room_for_info:
            yield make_godstring(religion, god_name, extra_info)
            allowed_info_c -= len( extra_info )
        else:
            yield make_godstring(religion, god_name)
    return


def get_some_sandwiches(num=1):
    with open(os.path.join(cwd, '..', 'corpora', 'data', 'foods', 'sandwiches.json')) as sandwiches_f:
        sandwiches_t = sandwiches_f.read()
    sandwiches = json.loads(sandwiches_t)['sandwiches']
    random.shuffle(sandwiches)
    for sd in sandwiches:
        if g_verbose and num < 10:
            desc = sd['description']
            print sd
            # if there are multiple sentences in the description, cut down to just the first sentence
            # (also strips ending periods)
            if desc.find('.'):
                desc = desc[:desc.find('.')]
            yield u'{name}: {desc}'.format(name=sd['name'], desc=desc)
        else:
            yield u'%s' % sd['name']


def get_simple_json(path, entry):
    with open(path) as f:
        data = f.read()
    items = json.loads(data)[entry]
    random.shuffle(items)
    for item in items:
        yield item


def get_some_foods(num=1):
    return get_simple_json(path=os.path.join(corpora_wd, 'foods', 'menuItems.json'), entry='menuItems')


def get_some_apples(num=1):
    return get_simple_json(path=os.path.join(corpora_wd, 'foods', 'apple_cultivars.json'), entry='cultivars')


def get_some_horses(num=1):
    return get_simple_json( path=os.path.join(corpora_wd, 'animals', 'horses.json' ), entry='horses' )


def get_some_dinosaurs(num=1):
    return get_simple_json( path=os.path.join(corpora_wd, 'animals', 'dinosaurs.json' ), entry='dinosaurs' )


def get_some_cats(num=1):
    return get_simple_json( path=os.path.join( corpora_wd, 'animals', 'cats.json' ), entry='cats' )

def get_some_birds(num=1):
    path = os.path.join( corpora_wd, 'animals', 'birds_north_america.json' )
    with open(path) as f:
        data = f.read()
    items = json.loads(data)['birds']
    birbs = []
    for item in items:
        family = item['family']
        for member in item['members']:
            birbs.append( (member, family) )
    random.shuffle(birbs)
    for entry in birbs:
        birb, family = entry
        if g_verbose:
            yield u'{name} ({fam})'.format(name=birb, fam=family)
        else:
            yield birb


def get_some_pokemon(num=1):
    for entry in get_simple_json(path=os.path.join(corpora_wd, 'games', 'pokemon.json'), entry='pokemon'):
        yield entry['name']


def get_some_elements(num=1):
    for entry in get_simple_json(path=os.path.join(corpora_wd, 'science', 'elements.json'), entry='elements'):
        yield entry['name']


def get_some_cities(num=1):
    for entry in get_simple_json(path=os.path.join(corpora_wd, 'geography', 'us_cities.json'), entry='cities'):
        if g_verbose:
            yield u'{city}, {state} (pop. {population})'.format(**entry)
        else:
            yield u'{city}, {state}'.format(**entry)
            

def get_some_colors(num=1):
    for entry in get_simple_json(path=os.path.join(corpora_wd, 'colors', 'crayola.json'), entry='colors'):
        if g_verbose:
            yield u'{color} ({hex})'.format(**entry)
        else:
            yield u'{color}'.format(**entry)


def get_some_celebs(num=1):
    return get_simple_json(path=os.path.join(corpora_wd, 'humans', 'celebrities.json'), entry='celebrities')

def get_some_moods(num=1):
    return get_simple_json(path=os.path.join(corpora_wd, 'humans', 'moods.json'), entry='moods')

def get_some_objects(num=1):
    return get_simple_json( path=os.path.join( corpora_wd, 'objects', 'objects.json' ), entry='objects' )

def get_some_plants(num=1):
    for entry in get_simple_json(path=os.path.join(corpora_wd, 'plants', 'plants.json'), entry='instruments'):  # ...instruments? OK
        if g_verbose:
            yield u'{name} ({species})'.format(**entry)
        else:
            yield u'{name}'.format(**entry)

def get_some_cocktails(num=1):
    return get_simple_json( path=os.path.join( corpora_wd, 'foods', 'iba_cocktails.json' ), entry='cocktails' )

def get_some_jobs(num=1):
    return get_simple_json( path=os.path.join( corpora_wd, 'humans', 'occupations.json' ), entry='occupations' )

def get_recipe_steps(num=1):
    """I am having way too much fun with this."""
    menu_items = list(get_simple_json(path=os.path.join( corpora_wd, 'foods', 'menuItems.json' ), entry='menuItems' ))
    foods = list()
    if random.random() < 0.3:
        foods += list(menu_items)
    foods += list(get_simple_json(path=os.path.join( corpora_wd, 'foods', 'fruits.json' ), entry='fruits' ))
    foods += list(get_simple_json(path=os.path.join( corpora_wd, 'foods', 'vegetables.json' ), entry='vegetables' ))
    foods += list(get_simple_json(path=os.path.join( corpora_wd, 'foods', 'condiments.json' ), entry='condiments' ))
    foods += list(get_simple_json(path=os.path.join( corpora_wd, 'foods', 'pizzaToppings.json' ), entry='pizzaToppings' ))
    foods += list(get_simple_json(path=os.path.join( corpora_wd, 'foods', 'herbs_n_spices.json' ), entry='herbs' ))
    foods += list(get_simple_json(path=os.path.join( corpora_wd, 'foods', 'herbs_n_spices.json' ), entry='spices' ))
    if random.random() < 0.05:
        foods += list(get_simple_json( path=os.path.join( corpora_wd, 'objects', 'objects.json' ), entry='objects' ))
    if random.random() < 0.02:
        foods += list(get_simple_json( path=os.path.join( corpora_wd, 'science', 'toxic_chemicals.json' ), entry='chemicals' ))

    recipe_ingredients = random.sample(foods, random.randint(2, num+1))
    recipe_title = random.choice( menu_items ).capitalize()
    adjs = list( get_simple_json( path=os.path.join( corpora_wd, 'words', 'adjs.json' ), entry='adjs' ) )
    if random.random() < 0.2:
        recipe_title = u'%s %s' % (random.choice(adjs).capitalize(), recipe_title)
    else:
        recipe_title = u'%s' % recipe_title
    prestr = recipe_title + u' [Ingredients: ' + ', '.join(recipe_ingredients) + ']'

    i = 0
    for entry in get_simple_json( path=os.path.join( corpora_wd, 'foods', 'combine.json' ), entry='instructions' ):
        random.shuffle(recipe_ingredients)
        i += 1
        stepstr = ('%d. ' % i) + entry.format(*recipe_ingredients).rstrip('.')
        if i == 1:
            stepstr = prestr + '  ' + stepstr
        yield stepstr

def get_some_gadgets(num=1):
    with open(os.path.join(cwd, "gadgets.txt")) as f:
        lines = f.readlines()
    random.shuffle(lines)
    for line in lines:
        gadget, desc = line.split(':')
        if g_verbose:
            yield u'{gadget}: {desc}'.format(gadget=gadget, desc=desc.strip('. '))
        else:
            yield gadget

def get_some_crimes(num=1):
    with open(os.path.join(cwd, "txt", "crimes.txt") ) as crime_f:
        crimes = crime_f.readlines()
    random.shuffle(crimes)
    for crime in crimes:
        yield crime.strip()

def get_some_babies(num=1):
    namezip_fn = os.path.join(cwd, 'txt', 'names.zip')
    namezip = zipfile.ZipFile(namezip_fn, 'r')
    inner_files = namezip.namelist()
    inner_files = filter(lambda s: s.endswith('.txt'), inner_files)
    while True:
        inner_fn = random.choice(inner_files)
        y = re.search('yob(\d{4})\.txt', inner_fn).group(1)
        with namezip.open(inner_fn) as name_f:
            names_txt = name_f.read()
        rows = names_txt.splitlines()
        if not g_verbose:
            row = random.choice(rows)
            name, gender, num = row.split(',')
            yield name
        else:
            # hoo boy
            f_names = m_names = dict()
            f_ranks = m_ranks = list()
            f_nums = m_nums = dict()
            for row in rows:
                name, gender, num = row.split( ',' )
                num = int(num)
                if gender == 'F':
                    N, R, M = f_names, f_ranks, f_nums
                else:
                    N, R, M = m_names, m_ranks, m_nums
                N[name] = num
                if num not in M:
                    M[num] = []
                M[num].append(name)
                if num not in R:
                    R.append(num)
            if random.random() < 0.5:
                pool, ranks, nums = f_names, f_ranks, f_nums
            else:
                pool, ranks, nums = m_names, m_ranks, m_nums
            name = random.choice(pool.keys())
            num_babies = pool[name]
            r = sorted(ranks, reverse=True).index(num_babies)
            tied = ''
            if len(nums[num_babies]) > 1:
                tied = 'T-'
            yield '%s (%s #%s%s)' % (name, y, tied, r)


def get_some_countries(num=1):
    return get_simple_json( path=os.path.join( corpora_wd, 'geography', 'countries.json' ), entry='countries' )


def get_some_diseases(num=1):
    symptoms = list(get_some_symptoms(num))

    for entry in get_simple_json(path=os.path.join(corpora_wd, 'medicine', 'diseases.json'), entry='diseases'):
        # each entry is a list of increasingly specific terms, so most specific term is most verbose
        if g_verbose:
            disease = entry[-1]
        else:
            disease = random.choice(entry)
        include_symptoms = random.random() < 0.5
        if include_symptoms:
            n = random.randint(1,2)
            symstr = ', '.join(random.sample(symptoms, n))
            yield '{disease} (symptoms: {symptoms})'.format(disease=disease, symptoms=symstr)
        else:
            yield disease


def get_some_symptoms(num=1):
    return get_simple_json( path=os.path.join( corpora_wd, 'medicine', 'symptoms.json' ), entry='symptoms' )


def get_some_sports(num=1):
    return get_simple_json( path=os.path.join( corpora_wd, 'sports', 'sports.json' ), entry='sports' )


def get_some_numbers(num=1):
    s0 = ("", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
    s1 = ("ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen")
    s2 = ("", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety")
    for i in range(num):
        p = random.random()
        if p < 0.5:
            n = random.randint(0, 100)
        elif p < 0.75:
            n = random.randint(100, 1000)
        else:
            n = random.randint(1000, 100000)
        if n == 0:
            yield "zero"
        elif n == 69:
            yield "69 >:D"
        elif n == 420:
            yield "420 >:D"
        elif n == 666:
            yield "666 >:D"

def get_some_greets(num=1):
    with open( os.path.join( cwd, "txt", "greetz.txt" ) ) as greetz_f:
        greetz = greetz_f.readlines()
    random.shuffle( greetz )
    for greet in greetz:
        yield greet.strip()


def thingsay(arg):
    """
    :param str arg:
    """
    global g_verbose
    import string
    arg = ''.join( filter( lambda c: c in string.printable, arg ) )
    re_arg = re.search( r"\s*(.+?)\s+(\w+(?:\s+steps)?)", arg )
    if not re_arg:
        # just bomb out, we might have been overzealous in triggering from IRC
        return
    num = re_arg.group(1)
    things = re_arg.group(2)
    thingnum, fmt_str = get_thing_fmt( num )
    printout = unicode(fmt_str.format(things=things))

    politeness_enabled = 'please' in arg.lower()
    g_verbose |= politeness_enabled
    polite_tag = ' %s, %s!' % (get_pleasantry(), get_friend().format(thing=things))

    if isinstance( thingnum, ZEROTHINGSRESPONSE ):
        # someone is being a real piece of work!!
        if politeness_enabled:
            printout += u' %s, %s!' % (get_pleasantry(), get_friend().format( thing=things ))
        return printout

    if thingnum > 20:
        face = ':/' if politeness_enabled else '>:('
        nope = get_unpleasantry()
        if thingnum > 20 and random.random() < 0.6:
            nope = get_thing_overflow_exception( things )
        spin = random.random()
        if politeness_enabled: spin -= 0.12345  # make polite option below more likely
        if spin < 0.0271828:
            return 'u should reconsider your behavior... i know you can do better, {guy}'.format( guy=get_friend() )
        elif spin < 0.55:
            return '{nope} NO {thing} FOR U {face}'.format( nope=nope, thing=things.upper(), face=face )
        elif spin < 0.6:
            return '{nope} THERE WILL BE NO {thing} FOR {jerk}S LIKE U {face}'.format( nope=nope.upper(),
                                                                                       jerk=get_dumdum().upper(),
                                                                                       thing=things.upper(), face=face )
        else:
            return 'You are a {jerk} and u get NO {things} {face}'.format( jerk=get_dumdum(), things=things.upper(),
                                                                           face=face )

    base_formatter = lambda c: c
    thing_formatters = {
        'god': make_godstring,
    }
    formatter = thing_formatters.get(things, base_formatter)

    if thingnum < 0 and 'u are a' in printout:
        if politeness_enabled:
            return printout + ", " + get_friend().format(thing=things) + "!!!!"
        else:
            return printout + " >:(!!!!"  # we are very cross now
    elif thingnum < 0:
        formatter = lambda c: ''.join( (reversed( base_formatter( c ) )) ).replace('(', '\x00').replace(')', '(').replace('\x00', ')')
        thingnum = abs( thingnum )

    thing_map = {
        'dogs': get_some_dogs,
        'gods': get_some_gods,
        'sandwiches': get_some_sandwiches,
        'foods': get_some_foods,
        'apples': get_some_apples,
        'horses': get_some_horses,
        'dinosaurs': get_some_dinosaurs,
        'cats': get_some_cats,
        'birds': get_some_birds,
        'pokemon': get_some_pokemon,
        'elements': get_some_elements,
        'cities': get_some_cities,
        'colors': get_some_colors,
        'celebrities': get_some_celebs,
        'moods': get_some_moods,
        'objects': get_some_objects,
        'plants': get_some_plants,
        'cocktails': get_some_cocktails,
        'jobs': get_some_jobs,
        'gadgets': get_some_gadgets,
        'recipe steps': get_recipe_steps,
        'crimes': get_some_crimes,
        'babies': get_some_babies,
        'countries': get_some_countries,
        'diseases': get_some_diseases,
        'sports': get_some_sports,
        'numbers': get_some_numbers,
        'greetings': get_some_greets,
    }
    def rando(n=1):
        nd = {_thing: gen(n) for (_thing, gen) in thing_map.items()}
        while True:
            k = random.choice(nd.keys())
            if k in ['things', 'recipe steps']:
                continue
            g = nd[k]
            it = g.next()
            yield '{s} ({thing})'.format(s=it, thing=k)
    thing_map['things'] = rando
    thing_map['recipes'] = get_recipe_steps
    printable_thing_map = thing_map.copy()
    for k,v in printable_thing_map.items():
        thing_map[k.rstrip('s')] = v
    if things in thing_map:
        getter = thing_map[things]
    else:
        return "Didn't recognize this thing: `{thing}` (supported things: {ok_things})".format(
            thing=things,
            ok_things=', '.join(sorted(["%s" % thing for thing in printable_thing_map.keys()]))
        )
    thingmax = int( math.ceil( thingnum ) )
    get_thing = getter(thingmax).next
    separator = ','
    if 'recipe' in things: separator = '.'

    s = printout + ' '
    i = thingnum
    while i > 1:
        s += formatter( get_thing() ) + separator + ' '
        i -= 1
    if thingnum <= 2:
        s = s.replace( separator, '' )
    if thingnum > 1:
        if 'recipe' not in things:
            s += 'and '
    last_thing = formatter( get_thing() )
    if i == 1:
        s += last_thing + '.'
    else:
        d_pct = int( i * len( last_thing ) )
        rev_chr = ''
        s += last_thing[:d_pct] + rev_chr + last_thing[d_pct:] + rev_chr + '.'
    if politeness_enabled:
        s += polite_tag
    # IRC cuts off lines at 510 characters, split into new lines if we barfed a lot of things
    import catread
    s = u'\r\n'.join(catread.format_lines(s, 500))
    return s


def serve_thingbarf(arg):
    """
    :param str arg:
    :return:
    """
    data = thingsay( arg )
    if not data:
        return False
    thingbarf_file = r'C:\tmp\thingbarf.txt'
    if os.path.exists( thingbarf_file ):
        os.unlink( thingbarf_file )
    if not os.path.exists( r'C:\tmp' ):
        os.makedirs( r'C:\tmp' )
    with codecs.open( thingbarf_file, 'w+', 'utf-8' ) as thingf:
        thingf.write( data.rstrip() )
    print repr(data)
    return True


if __name__ == "__main__":
    serve_thingbarf( ' '.join( sys.argv[1:] ) )