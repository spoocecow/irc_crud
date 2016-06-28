"""
Acrophobia playing IRC bot. Not great.
"""

import os, sys 
import socket, time
import random
from select import select

# these are options!!
network = 'irc.whatever.com'
port = 6667
_my_nick = 'ACROBOT'
_no_vote_nicks = []
_my_pw = 'mypass'
_my_quit_msg = "duh"
_THE_BOSS = 'stupid' # this is your name, stupid
chan = '#acro'

# these are global things because I'm lazy!!
endl = '\r\n'
chan_msg_begin = 'PRIVMSG ' + chan + ' :'
irc = None

def set_topic(topic):
    irc.send('TOPIC ' + chan + ' :' + topic + endl)

def send_chan_msg(msg):
    irc.send(chan_msg_begin + msg + endl)
    
def send_priv_msg(nick, msg):
    irc.send('PRIVMSG ' + nick + ' :' + msg + endl)
    
def send_notice(nick, msg):
    irc.send('NOTICE ' + nick + ' :' + msg + endl)

def connect(AcroBot, autostart=False):
    global irc
    irc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    irc.settimeout(10)
    irc.connect( (network, port) )
    irc.send( 'NICK '+_my_nick+endl )
    irc.send( 'USER '+_my_nick+" "+_my_nick+" "+_my_nick+" : glug"+endl )
    #time.sleep(5)
    data = irc.recv(4096)
    start = time.time()
    while ('recognized' not in data) and (time.time() < start+15):
        for line in data.split(endl):
            if 'PING' in line:
                    irc.send( 'PONG ' + line.split()[1] + endl )
        print data
        if 'protected' in data:
            irc.send( 'PRIVMSG NickServ :IDENTIFY ' + _my_pw + endl )
        data = irc.recv(4096)
    irc.send( 'JOIN '+chan+endl )
    print "####OK WE JOINED#####"
    if autostart:
        AcroBot.start()
    while True:
        time.sleep(0.01)
        pretime = time.time()
        if AcroBot.timeout > pretime:
            print pretime, "\tSetting socket timeout to ", AcroBot.timeout - pretime
            irc.settimeout( AcroBot.timeout - pretime )
        try:
            data = irc.recv(4096)
        except socket.timeout as e:
            print time.time(), "\ttimeout exception >:(", e
            pass
        #user_input, _, _ = select([sys.stdin], [], [], 0)
        #if user_input:
        #    send_chan_msg(user_input)
        readtime = time.time()
        
        for line in data.split(endl):
            if len(line) < 1: continue

            print time.time(), '\t', line

            if 'PING' in line:
                irc.send( 'PONG ' + line.split()[1] + endl )
                
            elif 'PRIVMSG' in line:
                nick = line[1:].split('!', 1)[0]
                msg = line.split(':', 2)[-1].strip()
                if 'PRIVMSG ' + _my_nick + ' :' in line:
                    AcroBot.receive_input(nick, msg)
                else:
                    respond_to_channel(AcroBot, nick, msg)
            elif 'PART' in line:
                nick = line[1:].split('!', 1)[0]
                if nick in AcroBot.players:
                    AcroBot.players.pop(nick)
                
        print time.time(), '\tDone parsing', data
        data = ''
                    
        if 0 < AcroBot.timeout < readtime:
                print time.time(), "Timeout! State transition should happen!"
                response = AcroBot.timeout_expired()
                if response:
                    send_chan_msg(response)

def respond_to_channel(bot, nick, msg):
    if '!acro' in msg:
        bot.receive_input(nick, '!acro')
    elif '!quit' in msg and nick == _THE_BOSS:
        bot.byebye()
    
class Player(object):
    def __init__(self, name):
        self.name = name
        self.entries = []
        self.most_recent_entry = ''
    
    def score(self):
        return sum([entry.score for entry in self.entries])
        
class Entry(object):
    def __init__(self, msg):
        self.msg = msg
        self.time = time.time()
        self.score = 0
    
    def __hash__(self):
        return hash(self.msg) + hash(self.time)
        
    def __cmp__(self, other):
        return cmp(self.score, other.score) or cmp(self.time, other.time)
    
class Acro:
    # states of play
    NOT_STARTED = 0
    GETTING_PLAYERS = 2
    DISPLAYING_ACRO = 4
    GETTING_ENTRIES = 8
    DISPLAYING_ENTRIES = 16
    GETTING_VOTES = 32
    DISPLAYING_VOTES = 64
    
    FACEOFF_STARTS_AT = 15
    FACEOFF_PARTICIPANTS = 2
    FACEOFF_ROUNDS = 3
    
    insults1 = ('dumb', 'stupid', 'idiot', 'moron', 'crap', 'poop', 'turd', 'stink', 'horse', 'jerk', 'cram')
    insults2 = ('face', 'head', 'ass', 'brain', '!!', 'weed', 'dancer', 'lover', ' kisser', 'horse')
    
    absent_player = Player('A jerk that left')
    
    # http://en.wikipedia.org/wiki/Letter_frequency#Relative_frequencies_of_the_first_letters_of_a_word_in_the_English_language
    # cheating a little bit to make some letters more common and some less common
    WEIGHTED_LETTERS = { 'A':4.2, 'B':4.0, 'C':4.1, 'D':3.1, 'E':4.0, 'F':3.0, 'G':3.0, 'H':3.5, 'I':2.7,
                         'J':1.5, 'K':1.3, 'L':4.0, 'M':4.1, 'N':3.9, 'O':3.2, 'P':4.0, 'Q':0.3, 'R':3.9,
                         'S':4.6, 'T':4.7, 'U':2.7, 'V':2.2, 'W':3.1, 'X':0.2, 'Y':3.0, 'Z':1.1 }
    
    def __init__(self):
        self.players = {}
        self.state = Acro.NOT_STARTED
        self.round_number = 0
        self.faceoff_round_number = 0
        self.this_rounds_entries = {} # {Player: 'My Funny Entry'}
        self.coded_entries = {} # {1: (Player, 'My Funny Entry')}
        self.this_rounds_votes = {} # {VotingPlayer: FunnyPlayer}
        self.acro = ''
        self.timeout = 0
        self.in_faceoff = False
        self.warned = False
        self.t_offset = lambda t: time.time() + t
        
    def reset(self):
        self.players = {}
        self.state = Acro.NOT_STARTED
        self.round_number = 0
        self.faceoff_round_number = 0
        self.this_rounds_entries = {} # {Player: 'My Funny Entry'}
        self.coded_entries = {} # {1: (Player, 'My Funny Entry')}
        self.this_rounds_votes = {} # {VotingPlayer: FunnyPlayer}
        self.acro = ''
        self.timeout = 0
        self.in_faceoff = False
        self.warned = False
        
    def start(self):
        if self.state == Acro.NOT_STARTED:
            self.reset()
            self.change_state( Acro.GETTING_PLAYERS )
            send_chan_msg( '*** Starting up, PM me to add yourself! ***' )
        
    def receive_input(self, nick, msg):
        if nick == _THE_BOSS:
            if msg.startswith('!say '):
                # hack to send chan msgs from owner
                send_chan_msg( msg[5:] )
            elif msg.startswith('!quit'):
                self.byebye()
        if self.state == Acro.NOT_STARTED and msg.startswith('!acro'):
            self.change_state( Acro.GETTING_PLAYERS )
            send_chan_msg( '*** Starting up, PM me to add yourself! ***' )
            self.players[nick] = Player(nick)
        elif self.state == Acro.GETTING_PLAYERS:
            self.players[nick] = Player(nick)
            send_priv_msg(nick, 'Ok, I added you.')
            self.timeout = self.t_offset(5)
        elif self.state == Acro.GETTING_ENTRIES:
            response = self.receive_acro(nick, msg)
        elif self.state == Acro.GETTING_VOTES:
            response = self.receive_vote(nick, msg)
            
    def change_state(self, state):
        print "Transitioning from %s -> %s" % (self.state, state)
        self.state = state
        if self.state == Acro.GETTING_PLAYERS:
            pass
        elif self.state == Acro.DISPLAYING_ACRO:
            self.change_state( Acro.GETTING_ENTRIES )
            acro = self.generate_acro()
            if self.in_faceoff:
                send_chan_msg( ' ### FACEOFF ROUND %d ### ' % (self.faceoff_round_number,) )
                set_topic(' ### FACEOFF ROUND ' + str(self.faceoff_round_number) + 
                         ' ### || The acro is:  ' + ' '.join( acro ) + '')
            else:
                set_topic('*** The acro is:  ' + ' '.join( acro ) + '  ***')
            send_chan_msg( '*** The acro is:  ' + ' '.join( acro ) + '  ***' )
            
        elif self.state == Acro.GETTING_ENTRIES:
            self.this_rounds_entries = {}
            for player in self.players.values():
                player.most_recent_entry = None
                player.most_recent_score = 0
            self.timeout = self.t_offset( 45 )
        elif self.state == Acro.DISPLAYING_ENTRIES:
            self.change_state( Acro.GETTING_VOTES )
            send_chan_msg( 'Here are the entries. Please PM me with the number you wish to vote for.' )
            # time, entry
            entries = self.this_rounds_entries.items()
            if len(entries) < 1:
                send_chan_msg( 'NO ENTRIES. WHAT THE HELL.' )
                self.change_state( Acro.DISPLAYING_VOTES )
                return
            random.shuffle(entries)
            self.coded_entries = dict(enumerate(entries))
            for i, pair in enumerate(entries):
                player, entry = pair
                player.most_recent_score = 0
                send_chan_msg( ' (%d)  %s' % (i+1, entry.msg) )
        elif self.state == Acro.GETTING_VOTES:
            self.this_rounds_votes = {}
            self.timeout = self.t_offset( 60 )
        elif self.state == Acro.DISPLAYING_VOTES:
            send_chan_msg( 'Voting is over!' )
            self.tabulate_votes()
            send_chan_msg( 'Next round will begin in 30 seconds. Talk amongst yourselves.')
            self.round_number += 1
            self.timeout = self.t_offset( 30 )
            
    def timeout_expired(self):
        output = ''
        if len(self.players) < 1:
            output = 'Nevermind, no players...'
            self.timeout = 0
            self.change_state( Acro.NOT_STARTED )
        elif self.state == Acro.GETTING_PLAYERS:
            self.change_state( Acro.DISPLAYING_ACRO )
        elif self.state == Acro.GETTING_ENTRIES:
            if not self.warned:
                self.warned = True
                self.warn_players()
            else:
                self.warned = False
                self.change_state( Acro.DISPLAYING_ENTRIES )
        elif self.state == Acro.GETTING_VOTES:
            self.change_state( Acro.DISPLAYING_VOTES )
        elif self.state == Acro.DISPLAYING_VOTES:
            self.change_state( Acro.DISPLAYING_ACRO )
        if output != '':
            return output
            
    def warn_players(self):
        send_chan_msg( '15 seconds remain! Remember, the acro is ' + self.acro)
        self.timeout = self.t_offset(15)
        
    def random_weighted_letter(self):
        # from http://stackoverflow.com/questions/352670/weighted-random-selection-with-and-without-replacement
        def WeightedSelectionWithoutReplacement(l):
            """Selects without replacement n random elements from a list of (item, weight) tuples."""
            total_weights = sum(float(x[1]) for x in l)
            L = sorted((random.random() * (float(x[1]) / total_weights), x[0]) for x in l)
            return L[-1][1]
        return WeightedSelectionWithoutReplacement( self.WEIGHTED_LETTERS.items() )
        
    def generate_acro(self):
        random_letter = lambda: chr( 
            random.choice(
                range( ord('A'), ord('Z') )
            )
        )
        acro_len = (self.round_number % 4) + 3
        acro = ''
        for i in range(acro_len):
            if random.random() < 0.3:
                acro += random_letter()
            else:
                acro += self.random_weighted_letter()
        self.acro = acro
        return self.acro
        
    def receive_acro(self, nick, msg):
        if nick not in self.players:
            self.players[nick] = Player(nick)
        if self.in_faceoff == True and self.players[nick] not in self.faceoff_participants:
            send_priv_msg(nick, "Shh! This is a faceoff, and YOU'RE NOT INVITED >:D")
            return
        split_msg = msg.split()
        if len(split_msg) != len(self.acro):
            send_priv_msg(nick, "The acro is %d letters and you gave me %d words, you %s!" % \
                ( len(self.acro), len(split_msg), self.generate_insult() )
            )
            return
        for i, word in enumerate(split_msg):
            aword = word.strip('"\'')
            if aword[0].upper() != self.acro[i]:
                send_priv_msg(nick, "%s does not begin with %s!" % (word, self.acro[i]) )
                return
        entry = Entry(msg)
        self.this_rounds_entries[ self.players[nick] ] = entry
        self.players[nick].most_recent_entry = entry
        send_priv_msg(nick, "Accepted, thanks :)")
        
    @staticmethod
    def generate_insult():
        return random.choice(Acro.insults1) + random.choice(Acro.insults2)
        
    def receive_vote(self, nick, vote):
        if nick not in self.players:
            self.players[nick] = Player(nick)
        try:
            vote = int(vote) - 1
        except ValueError:
            send_priv_msg(nick, "That's not even a number >:(" )
            return
        if vote not in self.coded_entries:
            send_priv_msg(nick, "That's not a number I gave you to vote for, %s!" % (self.generate_insult(),) )
            return
        voting_player = self.players[nick]
        voted_player, voted_entry = self.coded_entries[vote]
        if voting_player == voted_player:
            send_priv_msg(nick, "You can't vote for yourself!!! How dare you, %s. How dare you." % (nick,) )
            return
        elif voted_player.name in _no_vote_nicks:
            send_priv_msg(nick, "That's a bot entry actually!! Vote for an actual person if you can ok :3")

        self.this_rounds_votes[voting_player] = voted_player
        send_priv_msg(nick, "Vote counted, thanks :)")
        if len(self.this_rounds_votes) == len(filter(lambda player: player not in _no_vote_nicks, self.players)):
            # everyone's voted, short circuit
            self.timeout = 0
            self.timeout_expired()
            
    def tabulate_votes(self):
        for voted_player in self.this_rounds_votes.values():
            voted_player.most_recent_entry.score += 1
            
            
        full_vote_list = [ player for player in self.players.values() if player.most_recent_entry ]
        vote_list = [ player for player in self.players.values() if player.most_recent_entry and player.most_recent_entry.score > 0 ]
        round_winner = None
        fastest_entry = None
        if not self.in_faceoff:
            if len(self.this_rounds_votes) > 2:
                # sorts first by score, then time
                sorted_votes = sorted(full_vote_list)
                
                if sorted_votes[-1].most_recent_entry.score > sorted_votes[-2].most_recent_entry.score:
                    round_winner = sorted_votes[-1]
                    round_winner.most_recent_entry.score += 0.5
            if len(self.this_rounds_votes) > 1:
                # sort just by time
                fastest_entry = min(vote_list, key=lambda p: p.most_recent_entry.time)
                fastest_entry.most_recent_entry.score += 0.5

        send_chan_msg( 'Results for this round:' )
        send_chan_msg( '-----------------------' )
        
        full_vote_list.sort(key=lambda player: player.most_recent_entry)
        full_vote_list.reverse()
        
        for player in full_vote_list:
            player.entries.append( player.most_recent_entry )
            msg = (str(player.most_recent_entry.score) + '  ' + player.name + '   ').ljust(25) + \
                  player.most_recent_entry.msg
            if player is round_winner:
                msg += ' (most votes, +0.5)'
            if player is fastest_entry:
                msg += ' (fastest entry, +0.5)'
            send_chan_msg( msg )
        
        send_chan_msg(' ')
        send_chan_msg( 'Overall scores:' )
        send_chan_msg( '===============' )
        if self.in_faceoff:
            score_list = [(player.score(), player.name) for player in self.faceoff_participants]
        else:
            score_list = [(player.score(), player.name) for player in self.players.values()]
        score_list.sort()
        score_list.reverse()
        for score, name in score_list:
            send_chan_msg( '  ' + str(score) + '  ' + name )
        send_chan_msg(' ')
        
        if self.in_faceoff:
            self.faceoff_round_number += 1
            if self.faceoff_round_number > Acro.FACEOFF_ROUNDS:
                self.declare_winner()
        elif score_list[0][0] >= Acro.FACEOFF_STARTS_AT:
            send_chan_msg( '*** FACEOFF ***' )
            self.start_faceoff()
            
    def start_faceoff(self):
        players = self.players.values()
        players.sort(key=lambda player:player.score())
        players.reverse()
        competitors = players[:Acro.FACEOFF_PARTICIPANTS]
        if len(competitors) < 2:
            send_chan_msg( '*** NEVERMIND, not enough players >:( ***' )
            return
        else:
            self.in_faceoff = True
            send_chan_msg( '*** FACEOFF PARTICIPANTS: ***' )
            for participant in competitors:
                send_chan_msg( '*** ' + participant.name.center(21) + ' ***' )
            self.faceoff_round_number += 1 
            self.faceoff_participants = competitors
            
    def declare_winner(self):
        self.faceoff_participants.sort(key=lambda player:player.score())
        self.faceoff_participants.reverse()
        msg = '# ' + self.faceoff_participants[0].name.upper() + ' HAS WON!!! #'
        send_chan_msg('#' * len(msg))
        send_chan_msg(msg)
        send_chan_msg('#' * len(msg))
        send_chan_msg(' ')
        send_chan_msg('Thanks to all who participated! PM me to add yourself to the next round!')
        self.reset()
        self.round_number = 0
        self.change_state( Acro.GETTING_PLAYERS )
        
    def byebye(self):
        if len(self.players) > 0:
            send_chan_msg( 'Overall scores:' )
            send_chan_msg( '===============' )
            score_list = [(player.score(), player.name) for player in self.players.values()]
            score_list.sort()
            score_list.reverse()
            for score, name in score_list:
                send_chan_msg( '  ' + str(score) + '  ' + name )
            send_chan_msg(' ')
        send_chan_msg(_my_quit_msg)
        set_topic('!acro to start (if ' + _my_nick + ' is here...!)')
        sys.exit(0)
        
        
if __name__ == "__main__":
    AcroBot = Acro()
    try:
        connect(AcroBot, '-auto' in sys.argv)
    except KeyboardInterrupt:
        AcroBot.byebye()
        sys.exit(1)