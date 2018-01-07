# coding=utf-8
from __future__ import division
import math
import random
import re
import os, sys
import logging
import operator, string
import collections
from acrobot import Acro

g_log = logging.getLogger('catread')
shandle = logging.StreamHandler(stream=sys.stdout)
fhandle = logging.FileHandler('catread.log')
g_log.addHandler(shandle)
g_log.addHandler(fhandle)

WIDTH = 59

g_nickBlacklist = ['Colliwobble']
g_wordBlacklist = ['Klungo', '!logread', '!joke', '']


def format_lines_old(msg, maxwidth=WIDTH):
    lines = ['']
    line_num = len(msg) / maxwidth
    wordos = msg.split()
    words = []
    for w in wordos:
        temp_w = [w]
        if len(w) > (maxwidth/2): # long spammy line, go ahead and split
            mp = len(w) / 2
            temp_w = [ w[:mp], w[mp:] ]
        words.extend(temp_w)
    while words:
        if len(lines[-1]) >= maxwidth:
            lines.append('')
        word = words.pop(0)
        lines[-1] += word + ' '
    return map(str.strip, lines)


def format_lines(msg, maxwidth=WIDTH):
    lineno = math.ceil(len(msg) / maxwidth)
    if lineno >= 4:
        linelen = maxwidth
    else:
        linelen = (len(msg) / lineno) * 1.25  # allow for some wiggle room
    lines = ['']
    raw_words = msg.split()
    words = []
    for w in raw_words:
        max_word_width = linelen / 2
        if False:
        #if len(w) > max_word_width:
            # split long spammy words
            words.extend( [w[:max_word_width], w[max_word_width:] ] )
        else:
            words.append(w)
    for w in words:
        if (len(lines[-1]) + 1 +  len(w)) > linelen:
            lines.append('')
        lines[-1] += ' ' + w
    return map(str.strip, lines)



def catsay(msg, nick='A Cat', date=''):
   catfmt = r"""
                   {0}
7 _        /|__/\   {1}
7//_______/ .  . \  {2}
7\  C   T     i  / <{3}
7 \   A        |    {4}
7 | ||     | ||     {5}
7 |__\\    |__\\    {6}
   """
   lines = format_lines(msg, WIDTH)
   print lines
   if len(lines) > 5:
      g_log.error("This was too long: %s", msg)
      return None
   balloon_width = max( map(len, lines) )
   top_line = ' ' + '_' * (balloon_width+2) + ' '
   bottom_line = '\\' + '_' * (balloon_width+2) + '/'
   blank_line = ''
   fmted_lines = ['| %s |' % line.center(balloon_width) for line in lines]
   middle_line_i = 3
   vertical_centered_lines = [top_line] + fmted_lines[:] + [bottom_line]
   while len(vertical_centered_lines) < 7:
      if len(vertical_centered_lines) % 2 == 0:
         vertical_centered_lines.append(blank_line)
      else:
         vertical_centered_lines.insert(0, blank_line)
         vertical_centered_lines.append(blank_line)
   assert len(vertical_centered_lines) == 7, "zuhh? %d" % len(vertical_centered_lines)
   vertical_centered_lines[middle_line_i] = ' ' + vertical_centered_lines[middle_line_i][1:]
   if vertical_centered_lines[-1] == blank_line:
       if date:
           vertical_centered_lines[-1] =  ('~ %s, %s' % (nick, date)).rjust(balloon_width+4)
       elif nick:
           vertical_centered_lines[-1] =  ('~ %s' % nick).rjust(balloon_width+4)
       else:
           vertical_centered_lines[-1] =  ('~ %s' % nick).rjust(balloon_width+4)
   return catfmt.format(
      *vertical_centered_lines, width=balloon_width
   )

def sanitize(line):
    import string
    return filter(lambda c: c in string.printable, line)

def is_line_bad(nick, text):
    if nick in g_nickBlacklist:
        return True
    for bl_word in g_wordBlacklist:
        if bl_word in text:
            return True
    return False

def get_line(log=r"C:\Users\Mark\AppData\Roaming\mIRC\logs\#banjo-kazooie.DorksNet.log"):
    with open(log) as logfile:
        lines = logfile.readlines()
        line_bad = True
        is_speech = re.compile(
            r"""
            [¡\[]?(?P<timestamp>\d\d:\d\d[:.]\d\d)[\]!] # timestamp
            \s+<[\s\d]*(?P<nick>[\w\d_\\]+).*>  # nick
            \s+(?P<text>.*)\s*
            """,
            re.IGNORECASE | re.MULTILINE | re.VERBOSE
        )
        original_line = random.choice(lines)
        line = sanitize( original_line.strip() )
        while line_bad:
            print "line=", line
            match = is_speech.search(line)
            if match:
                nick = match.group('nick')
                text = match.group('text')
                tstamp = match.group('timestamp')
                if is_line_bad(nick, text):
                    g_log.info( "this line bad: %s", line)
                elif text.startswith('!'):
                    # boring read bad I hate it
                    g_log.debug("this line boring: %s", line)
                else:
                    g_log.info("Good: %s", match.groupdict())
                    info = match.groupdict()
                    try:
                        date = tstamp + ' ' + find_date(original_line, lines)
                    except ValueError:
                        date = ''
                    info['date'] = date
                    return info
            original_line = random.choice(lines)
            line = sanitize( original_line.strip() )
        return {}

def find_date(line, loglines):
    line_i = loglines.index(line)
    date = ''
    for log_l in reversed(loglines[:line_i]):
        if log_l.startswith('Session Start:'):
            _, _, wd, m, d, t, y = log_l.split()
            return '%s %s %s' % (m,d,y)

def get_logfile():
    default = r"C:\Users\Mark\AppData\Roaming\mIRC\logs\#banjo-kazooie.DorksNet.log"
    other_log_dir = r"C:\Users\Mark\Desktop\Stupid Crap\java\markovbot\logs"
    log_files = os.listdir(other_log_dir)
    chance = random.random() > 0.3
    if log_files and chance:
            return os.path.join(other_log_dir, random.choice(log_files))
    return default



def get_catread(data):
    if data:
        line = data
        msg = catsay(line)
    else:
        logfile = get_logfile()
        retries = 5
        msg = None
        while not msg:
            line_info = get_line(log=logfile)
            line = line_info.get('text')
            nick = line_info.get('nick')
            date = line_info.get('date')
            msg = catsay(line, nick, date)
            retries -= 1
            if retries < 0:
                return ''
    if msg.startswith('\n'):
        msg = msg[1:]
    while re.match('^\s+$', msg, re.MULTILINE | re.UNICODE):
        print "Choppin' a line"
        msg = msg[msg.find('\n')+1:]
    return msg

def serve_catread(data=None):
    retries = 5
    data = None
    while not data:
        data = get_catread(data)
        retries -= 1
        if retries <= 0:
            data = 'crap'
            break
    catread_file = r'C:\tmp\catread.txt'
    if os.path.exists(catread_file):
        os.unlink(catread_file)
    if not os.path.exists(r'C:\tmp'):
        os.makedirs(r'C:\tmp')
    with open(catread_file, 'w+') as catf:
        catf.write(data.rstrip())
    return True

def reelfun():
    P = { # 0sym 1sym  2sym  3sym
        1: [.85, .023, .025, 0.001], # reel 1
        2: [.67, .034, .035, 0.002], # reel 2
        3: [.88, .045, .045, 0.003], # reel 3
        4: [.85, .066, .055, 0.004], # reel 4
        5: [.34, .087, .065, 0.005]  # reel 5
    }
    reels = 5
    symbols = 4

    import operator
    import itertools
    combos = [c for c in itertools.product( range(symbols), repeat=reels)]
    symbol_sums = {}
    for c in combos:
        symcount = sum(c)
        if symcount not in symbol_sums:
            symbol_sums[symcount] = []
        probs = [P[reel+1][syms] for reel, syms in enumerate(c)]
        symbol_sums[symcount].append(probs)
    for count in sorted(symbol_sums):
        for method in sorted(symbol_sums[count]):
            print count, method, 'hitrate%:', '%0.10f' % reduce(operator.mul, method, 100)

def simspins(p=1.0, n=10**6, slots=4):
    import random
    c = random.randint(1,slots+1)
    if c == 1:
        return simspins(p+1, n-1, slots)
    else:
        p = c
    return p

def orderit(it, ordered_it, permutation):
    translation = dict()


if __name__ == '__main__':

    if sys.argv:
        serve_catread(' '.join(sys.argv[1:]))
    else:
        serve_catread()
    print '-' * 120
    print open(r'C:\tmp\catread.txt').read()