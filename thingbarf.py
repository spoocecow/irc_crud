# coding=utf-8
from __future__ import division
import codecs
import math, cmath
import inspect
import json
import os, sys
import random
import re
from acrobot import Acro

_thisfile = inspect.getfile( inspect.currentframe() )
cwd = os.path.dirname( os.path.abspath( _thisfile ) )

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
            'twenty': 20}
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
        existential_questions = (
            'Why did you want no {{things}}?',
            'No {{things}}? Why?',
            'No {{things}}? At all? Why?',
            'Why must you try me so? I am a humble script and handling zero is hard for me.',
            "I don't know why you want this. Here are no {{things}}.",
            'I exist to serve {{things}}. Please request some {{things}}, or leave me in peace.',
            "I don't mean to be rude, but I truly do not understand why you are asking for exactly zero {{things}}.",
            "No {{things}}... this request is a mystery to me. In my humble opinion, you should ask for some {{things}}.",
            "Perhaps there truly is evil in the world. Why would you ask, specifically, for no {{things}}?",
            "Here are zero {{things}}. ---->                                <---  I hope you are happy.",
            "No {{things}}? For you, my friend, I will fulfill this request.",
            "No {{things}}? For you, sir or madam, I will gladly fulfill this request.",
            "No {{things}}? For you, stranger, I will grudgingly fulfill this request.",
        )
        return ZEROTHINGSRESPONSE(), random.choice( existential_questions )
    elif thingnum % 1 != 0:
        retfmt = 'Here {plur} {thingnum:.2f} {{things}}:'
    return thingnum, retfmt.format( thingnum=thingnum, plur=plur )


def get_some_dogs(num=1):
    with open( os.path.join(cwd, "txt", "dogs.txt") ) as dogf:
        dogs = dogf.readlines()
    dog_selections = random.sample( xrange( len( dogs ) ), num )
    for dog_choice in dog_selections:
        yield dogs[dog_choice].strip()


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
            yield religion, god_name, extra_info
            allowed_info_c -= len( extra_info )
        else:
            yield religion, god_name, ''
    return


def get_some_sandwiches(num=1):


def make_godstring(arg):
    religion, god, info = arg
    if g_verbose:
        retstr = u"{godname}".format( godname=god )
    else:
        retstr = u"{godname}".format( godname=god )

    if info:
        retstr += u' - {info}'.format( info=info )

    if g_verbose:
        retstr += u' ({religion})'.format( religion=religion )
    return retstr


def thingsay(arg):
    """
    :param str arg:
    """
    global g_verbose
    import string
    arg = ''.join( filter( lambda c: c in string.printable, arg ) )
    re_arg = re.search( r"\s*(.+?)\s+(\w+)s?", arg )
    num = re_arg.group(1)
    thing = re_arg.group(2)
    thingnum, fmt_str = get_thing_fmt( num )
    printout = fmt_str.format(thing=thing)

    politeness_enabled = 'please' in arg.lower()
    g_verbose |= politeness_enabled
    polite_tag = ' %s, %s!' % (get_pleasantry(), get_friend())

    if thingnum == 0 or thingnum > 20:
        things = thing + 's'
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
    formatter = thing_formatters.get(thing, base_formatter)

    if thingnum < 0 and 'u are a' in printout:
        if politeness_enabled:
            return printout + ", " + get_friend() + "!!!!"
        else:
            return printout + " >:(!!!!"  # we are very cross now
    elif thingnum < 0:
        formatter = lambda c: ''.join( (reversed( base_formatter( c ) )) )
        thingnum = abs( thingnum )
    elif isinstance( thingnum, ZEROTHINGSRESPONSE ):
        # someone is being a real piece of work!!
        if politeness_enabled:
            printout += ' %s, %s!' % (get_pleasantry(), get_friend())
        return printout

    thing_map = {
        'dog': get_some_dogs,
        'god': get_some_gods
    }
    if thing in thing_map:
        getter = thing_map[thing]
    else:
        return "Didn't recognize this thing: {thing} (supported things: {things})".format(
            thing=thing,
            things=', '.join(thing_map.keys())
        )
    thingnum = int( math.ceil( thingnum ) )
    get_thing = getter(thingnum).next

    s = printout + ' '
    i = thingnum
    while i > 1:
        s += formatter( get_thing() ) + ', '
        i -= 1
    if thingnum <= 2:
        s = s.replace( ',', '' )
    if thingnum > 1:
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
    print data
    return True


if __name__ == "__main__":
    serve_thingbarf( ' '.join( sys.argv[1:] ) )