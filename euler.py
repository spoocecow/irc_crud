#coding=utf-8
# mwn.  summer 2008-2009

import time
import itertools
import decimal
import random
import math
from math import sqrt
from math import floor
from math import log
import sys

def findPrimesTo(n):
    """Sieve of Eratosthenes"""
    list = range(0,n)
    lim = sqrt(n)
    prime = 2
    while prime < lim:
        for i in xrange(prime,n,prime):
            list[i] = 0
        list[prime] = prime
        PP = prime+1
        while list[PP] == 0:
            PP += 1
        prime = PP
    primes = [i for i in list if i != 0]
    primes.remove(1)
    return primes

def isPrime(n, easyprimes=findPrimesTo(100)):
    if n == 1:
        return False
    # initial easy test
    for prime in easyprimes:
        if prime > n:
            break
        if n == prime:
            return True
        elif n % prime == 0:
            return False
    # tougher test
    lowbound = len(easyprimes)/6
    d1 = lambda x: (6 * x) + 1
    d2 = lambda x: (6 * x) - 1
    for i in xrange(lowbound, sqrt(n)):
        if n % d1(i) == 0:
            return False
        if n % d2(i) == 0:
            return False
    return True

def numDigits(n):
    return int( log(n,10) ) + 1

def sumDigits(n):
    sum = 0
    while n > 0:
        sum += n%10
        n /= 10
    return sum

def getDigits(n):
    list = []
    m = n
    while m > 0:
        list.insert(0,m%10)
        m /= 10
    return list

def findDivisors(n):
    d = 0
    for i in range(1,sqrt(n)):
        if n%i == 0:
            d += 2
    return d

def gimmeDivisors(n):
    l = [1]
    for i in range(2,sqrt(n)+1):
        if n%i == 0:
            l.append(i)
            if i != sqrt(n):
                l.append(n/i)
    return l

def primeFactors(n, primes=[]):
    l = []
    if n < 2:
        return l
    if primes == []:
        primes = findPrimesTo(n+1)

    for i in primes:
        if i > n:
            break
        if n%i == 0:
            l.append(i)
            n = n/i

    return l

def primeFactorsWithExp(n, primes=[]):
    l = {}
    if primes == []:
        primes = findPrimesTo(n)
    for i in primes:
        while n%i == 0:
            if i not in l:
                l[i] = 1
            else:
                l[i] += 1
            n = n/i
    return l

def l2i(l):
    return reduce(lambda a,d: 10*a+d, l, 0)

def i2l(n):
    """Basically the same as getDigits"""
    l = []
    m = n
    while m > 0:
        l.insert(0,m%10)
        m /= 10
    return l

def testfunction(obj, function, args, repetitions=100):
    """testfunction(euler, "primeFactors", (1234567, primes), [repeat=1000])"""
    total = 0
    for i in range(repetitions):
        t = time.time()
        F = getattr(obj,function)
        ret = F(*args)
        total += (time.time()-t)
    print "Average time:",(total/repetitions)
    return ret

def totient(n, factors=[],primes=[]):
    """The totient of a positive integer n is defined to be 
    the number of positive integers less than or equal to n 
    that are coprime to n."""
    if factors == []:
        factors = primeFactors(n,primes)
    from operator import mul
    omega = lambda x: (1.0 - (1.0/x))
    return n * reduce(mul, map(omega, factors), 1)

def factorial(n):
    return reduce (lambda x,y: x*y, range(1, n+1,), 1)

def choose(n,r):
    """n choose r"""
    return factorial(n) / (factorial(r) * factorial(n-r))

def gcd(a,b):
    while b > 0:
        a,b = b, a%b
    return a

def baseN(num,b):
    return ((num == 0) and  "0" ) or ( baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])

def permute (seq, k=1):
    "Returns the kth permutation of seq (in lexicographic order)"
    seqc = seq[:]
    result = []
    fact = factorial(len(seq))
    k %= fact
    while seqc:
        fact = fact / len (seqc)
        choice, k = k // fact, k % fact
        result += [seqc.pop (choice)]
    return result

def isPermutation(x,y):
    """Returns true if x is a permutation of y."""
    l = x[:]
    m = y[:]
    for a in l:
        if a in m:
            m.remove(a)
        else:
            return False
    m = y[:]
    for a in m:
        if a in l:
            l.remove(a)
        else:
            return False
    return True
    
def isPandigital(*args):
    """Returns true if all args comprise digits 1-9"""
    digits = range(1,10)
    for a in args:
        a_digits = getDigits(a)
        for a_d in a_digits:
            if a_d in digits:
                digits.remove(a_d)
            else:
                return False
    return len(digits) == 0
    
def int_concat(*args):
    """Concatenate given numbers, left to right, returning int"""
    start = 0
    res = 0
    for a in reversed(args):
        res += a * (10 ** start)
        start += int(log(a, 10)) + 1
    return res

def reverseDigits(n):
    return int(str(n)[::-1])

BASE2 = "01"
BASE10 = "0123456789"
BASE16 = "0123456789ABCDEF"
def baseconvert(number,fromdigits,todigits):
    if str(number)[0]=='-':
        number = str(number)[1:]
        neg=1
    else:
        neg=0

    # make an integer out of the number
    x=long(0)
    for digit in str(number):
       x = x*len(fromdigits) + fromdigits.index(digit)

    # create the result in base 'len(todigits)'
    res=""
    while x>0:
        digit = x % len(todigits)
        res = todigits[digit] + res
        x /= len(todigits)
    if neg:
        res = "-"+res

    return res


###############################################################################
###############################################################################
############################## P R O B L E M S ################################
###############################################################################
###############################################################################

def prob12():
    """What is the value of the first triangle number to have over 500 divisors?"""
    a = 1
    t1 = time.time()
    tri = 1
    div = findDivisors(tri)
    while(div < 500):
        #if div > 200:
        #    print tri
        a += 1
        tri += a
        div = findDivisors(tri)
    print tri,time.time()-t1

def isSquare(n):
    return n != 1 and floor(sqrt(n))**2 == n

def prob15():
    """Starting in the top left corner in a 20x20 grid, how many routes are there to the bottom right corner?"""
    print "40!/(20!(40!-20!))"

def prob16():
    """What is the sum of the digits of the number 2**1000?"""
    print sumDigits(2**1000)

def prob19():
    """How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?"""
    century = 0
    months = [0,3,3,6,1,4,6,2,5,0,3,5]
    leapmonths = [6,2,3,6,1,4,6,2,5,0,3,5]
    sundays = 0
    for year in range(1901,2000):
        y = year % 100
        c = 0
        leap = False
        if year % 4 == 0:
            leap = True
        Y = y + floor(y/4)
        sum = c + y + Y
        for month in range(0,12):
            print "checkin'", (month+1),"/",year
            s = sum + 1
            if leap:
                s += leapmonths[month]
            else:
                s += months[month]
            if s % 7 == 0:
                sundays += 1
                print "!!!"

    return sundays + 1


def hop(i,jump,lim):
    if i >= lim:
        return lim
    if isSquare(i):
        jump += 2
    return i + hop(i+jump,jump,lim)

def prob28(n):
    """What is the sum of both diagonals in a 1001x1001 spiral?"""
    return hop(1,2,n**2)

def sumList(l):
    sum = 0
    for x in l:
        sum += x
    return sum

def prob21(n):
    """Evaluate the sum of all amicable pairs under 10000."""
    sums = {}
    ans = 0
    for i in range(1,n):
        factors = gimmeDivisors(i)
        sfact = sumList(factors)
        if i in sums and sums[i] == sfact:
            ans += i
            ans += sfact
        else:
            sums[sfact] = i
    return ans

def allDigitsUnique(n):
    digits = [0,1,2,3,4,5,6,7,8,9]
    useddigits=[]
    if n < 1000000000:
        useddigits.append(0)
    while n>0:
        d = n%10
        if d in useddigits:
            return False
        useddigits.insert(0,d)
        n = n / 10
    return True

def all_perms(str):
    if len(str) <=1:
        yield str
    else:
        for perm in all_perms(str[1:]):
            for i in range(len(perm)+1):
                yield perm[:i] + str[0:1] + perm[i:]

def prob23():
    """A perfect number is a number for which the sum of its proper divisors is exactly equal to the number. For example, the sum of the proper divisors of 28 would be 1 + 2 + 4 + 7 + 14 = 28, which means that 28 is a perfect number.

    A number whose proper divisors are less than the number is called deficient and a number whose proper divisors exceed the number is called abundant.

    As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the smallest number that can be written as the sum of two abundant numbers is 24. By mathematical analysis, it can be shown that all integers greater than 28123 can be written as the sum of two abundant numbers. However, this upper limit cannot be reduced any further by analysis even though it is known that the greatest number that cannot be expressed as the sum of two abundant numbers is less than this limit.

    Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers."""
    possibles = dict( [ (x,1) for x in range(12,28123) if sum(gimmeDivisors(x)) > x] )
    asum = 0
    for i in range(1,28123):
        summable = False
        for p in possibles:
            if p > i:
                break
            if (i-p) in possibles:
                #print i,"can be summed!\t",p,"+",(i-p)
                summable = True
                break
        if not summable:
            asum += i
            #print i,"not summable."
    return asum

def prob24(n=1000000):
    """What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?"""
    digits = [0,1,2,3,4,5,6,7,8,9]
    return permute(digits,n)

def prob26(n=1000):
    """Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part."""
    longest = 0
    longest_n = 0
    for i in range(2,n):
        # do out the long division manually
        res = -1
        rem = -1
        numerator = 1
        result_chain = []
        while rem != 0:
            numerator *= 10
            res = numerator / i
            rem = numerator % i
            numerator = rem
            if (res, rem) in result_chain:
                # cycle found, calculate length
                cycle_begin = result_chain.index( (res,rem) )
                cycle_len = len(result_chain) - cycle_begin
                if cycle_len > longest:
                    print '\t', i, "is new longest!"
                    longest = cycle_len
                    longest_n = i
                break
            else:
                result_chain.append( (res,rem) )
    return longest_n

def prob27(x):
    """Considering quadratics of the form:
    n**2 + an + b, where |a|< 1000 and |b| < 1000

    Find the product of the coefficients, a and b, for the quadratic expression that produces the maximum number of primes for consecutive values of n, starting with n = 0."""
    greatest = 0
    ga = 0
    gb = 0
    for a in xrange(-x,x):
        for b in xrange(-x,x):
            f = lambda n: n**2 + (a*n) + b
            n = 0
            if a is 0 and b is 0:
                continue
            while isPrime(abs(f(n))):
                n += 1
            if n > greatest:
                greatest = n
                ga = a
                gb = b
    print "n^2 +",ga,"n +",gb," produces",greatest,"primes."
    return ga * gb


def prob29(n):
    """How many distinct terms are in the sequence generated by a**b for 2<a,b<100?"""
    list = []
    for a in range(2,n+1):
        for b in range(2,n+1):
            x = a**b
            if x not in list:
                list.append(x)
    return len(list)


def prob30():
    """Find the sum of all the numbers that can be written as the sum of the fifth powers of their digits."""
    total = 0
    for i in range(9,500000):
        l = getDigits(i)
        l = [u**5 for u in l]
        tsum = sum(l)
        if tsum == i:
            print i
            total += i
    return total

def prob31(n=200):
    """In England the currency is made up of pound, $, and pence, p, and there are eight coins in general circulation:
    1p, 2p, 5p, 10p, 20p, 50p, $1 (100p) and $2 (200p).

    It is possible to make $2 in the following way:
    1x$1 + 1x50p + 2x20p + 1x5p + 1x2p + 3x1p

    How many different ways can $2 be made using any number of coins?
    """
    coins = [1,2,5,10,20,50,100,200]
    ways = 0
    while coins:
        largest = coins.pop(-1)
        sum = largest
        remaining_coins = coins[:]
        while sum < n:
            pass
    pass
    
def prob32():
    """
    We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once; for example, the 5-digit number, 15234, is 1 through 5 pandigital.

    The product 7254 is unusual, as the identity, 39 x 186 = 7254, containing multiplicand, multiplier, and product is 1 through 9 pandigital.

    Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.

    HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum.
    """
    pandigital_products = set()
    for a in range(1,100):
        for b in range(100, 9999):
            c = a * b
            if c > 9999:
                break
            if isPandigital(a,b,c):
                pandigital_products.add(c)
    return sum(list(pandigital_products))

def prob33():
    """The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting to simplify it may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.

    We shall consider fractions like, 30/50 = 3/5, to be trivial examples.

    There are exactly four non-trivial examples of this type of fraction, less than one in value, and containing two digits in the numerator and denominator.

    If the product of these four fractions is given in its lowest common terms, find the value of the denominator."""
    for de in range(11,100):
        for nu in range(10,de):
            sol = (1.0 * nu) / de
            dd = getDigits(de)
            nd = getDigits(nu)
            for d in dd:
                if d in nd and d != 0:
                    N = nd[:]
                    D = dd[:]
                    N.remove(d)
                    D.remove(d)
                    if D[0] == 0:
                        continue
                    ssol = (1.0 * N[0]) / D[0]
                    if abs(ssol - sol) < 0.00001:
                        print nu,"/",de,"=",sol,"\n\t",
                        print N[0], "/",D[0], "=",ssol,"\n"


def prob34(n):
    """Find the sum of all numbers which are equal to the sum of the factorial of their digits."""
    total = 0
    #         0 1 2 3 4   5   6   7     8     9
    ftable = [1,1,2,6,24,120,720,5040,40320,362880]
    C = 8
    for i in itertools.count(9):
        if i > n:
            break
        C += 1
        if C == 100000:
            print i
            C = 0
        l = getDigits(i)
        l = [ftable[u] for u in l]
        tsum = sum(l)
        if tsum == i:
            print i
            total += i
    return total


def prob35(n=1000000):
    """The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719, are themselves prime.

    There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

    How many circular primes are there below one million?"""
    primes = dict([(x,1) for x in findPrimesTo(n)])
    circprimes = {}
    def rotate(l):
        l.insert(0, l.pop())
        return l
    S = [1,2,3,4,5]
    num = 4 # for 2,3,5,7
    for i in range(11, n):
        if i in circprimes:
            print i,"is circular prime already hashed!!!!"
            num += 1
        elif i in primes:
            l = []
            s = getDigits(i)
            for a in range(len(s)):
                rotate(s)
                l.append(s[:])
            circOK = True
            for p in l:
                if not isPrime(l2i(p), primes):
                    circOK = False
                    break
            if circOK:
                print i,"is circular prime!"
                for p in l:
                    circprimes[l2i(p)] = 1
                num += 1
    return num

def prob36():
    """Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.
(Please note that the palindromic number, in either base, may not include leading zeros.)"""
    sum = 0
    for x in xrange(1,1000000):
        sx = str(x)
        xb = baseconvert(sx,BASE10,BASE2)
        if sx[::-1] == sx and xb[::-1] == xb:
            print x,"is palindrome! (binary =",xb,")"
            sum += x
    return sum

def prob37(n=1000000):
    """The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits from left to right, and remain prime at each stage: 3797, 797, 97, and 7. Similarly we can work from right to left: 3797, 379, 37, and 3.

    Find the sum of the only eleven primes that are both truncatable from left to right and right to left."""
    sum = 0
    count = 11
    primes = dict([(x,1) for x in findPrimesTo(n)])
    for i in xrange(11,n):
        if count is 0:
            break
        if i in primes:
            s = getDigits(i)
            rt = [s[x:] for x in range(1,len(s))]
            OK = True
            for m in rt:
                if l2i(m) not in primes:
                    OK = False
                    break
            if OK is True:
                lt = [s[:x] for x in range(1,len(s))]
                for n in lt:
                    if l2i(n) not in primes:
                        OK = False
                        break
                if OK is True:
                    print "wowee, found one:", i
                    count -= 1
                    sum += i
                    print "(",count," more to go)"
    return sum
    
def prob38():
    """
    Take the number 192 and multiply it by each of 1, 2, and 3:

    192 x 1 = 192
    192 x 2 = 384
    192 x 3 = 576
    By concatenating each product we get the 1 to 9 pandigital, 192384576. We will call 192384576 the concatenated product of 192 and (1,2,3)

    The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).

    What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product of an integer with (1,2, ... , n) where n > 1?
    """
    largest = 0
    i = 2
    lim = 999999999 / 2
    for i in xrange(2 ,10000):
        for range_len in xrange(2, i):
            if i * range_len > lim:
                break
            products = []
            _prod = 0
            for _a in xrange(1,range_len):
                _prod = i * _a
                if _prod > 98765:
                    break
                products.append( _prod )
            concat = int_concat(*products)
            if concat > 987654321:
                break
            if isPandigital(concat):
                print "[1..%d] * %d = %d" % (range_len, i, concat)
                if concat > largest:
                    largest = concat
    return largest
            

def prob39(n=1001):
    """If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are exactly three solutions for p = 120.

    {20,48,52}, {24,45,51}, {30,40,50}

    For which value of p <= 1000, is the number of solutions maximised?"""
    best = 0
    bestp = 1
    for p in range(4,n):
        ptry = 0
        print p
        cdict = {}
        for a in range (1,p-2):
            for b in range (1,p-2):
                c = p - a - b
                if c not in cdict and a**2 + b**2 == c**2:
                    print "\t{",a,",",b,",",c,"}"
                    ptry += 1
                    cdict[c] = 1
        if ptry > best:
            best = ptry
            bestp = p
    return bestp

def prob40():
    """Finding the nth digit of the fractional part of the irrational number."""
    s = ""
    for i in range(1,1000000):
        s += str(i)
    print s[1:4]
    n = int(s[0:1]) * int(s[9:10]) * int(s[99:100]) * int(s[999:1000])
    n = n * int(s[9999:10000]) * int(s[99999:100000]) * int(s[999999:1000000])
    return n

def prob41(n=7):
    """We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is also prime.

What is the largest n-digit pandigital prime that exists?"""
    digits = [1,2,3,4,5,6,7,8,9]
    primes = dict([(x,1) for x in findPrimesTo(10**n)])
    print "done primes"
    largest = 0
    for j in range(2,n+1):
        D = digits[:j]
        N = D[:]
        for i in range(factorial(j)):
            q = l2i(N)
            if q in primes and q > largest:
                largest = q
            N = permute(D,i)
    return largest


def prob42(filename="words.txt"):
    """The nth term of the sequence of triangle numbers is given by, tn = (1/2)n(n+1); so the first ten triangle numbers are:

    1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

    By converting each letter in a word to a number corresponding to its alphabetical position and adding these values we form a word value. For example, the word value for SKY is 19 + 11 + 25 = 55 = t10. If the word value is a triangle number then we shall call the word a triangle word.

    Using words.txt (right click and 'Save Link/Target As...'), a 16K text file containing nearly two-thousand common English words, how many are triangle words?"""
    import pickle
    newfile = file(filename)
    #l = newfile.readlines()
    words = [a.strip("\"\n") for a in newfile.readlines()[0].split(",")]
    tri = lambda n: 0.5 * n * (n+1)
    triangles = dict([(tri(n),n) for n in range(1,27)])
    tsum = 0
    for w in words:
        #print w
        value = sum(map(lambda a: ord(a) - 64,w))
        if value in triangles:
            tsum += 1
    return tsum

def prob43():
    o = [0,1,2,3,4,5,6,7,8,9]
    n = o[:]
    p = [2,3,5,7,11,13,17]
    total = 0
    r = range(7)[::-1]
    i = 1
    max = factorial(10)
    while i < max:
        good = True
        for j in r:
            chunk = l2i(n[j+1:j+4])
            if ( chunk % p[j] ) != 0:
                good = False
                break
        if good:
            print l2i(n)
            total += l2i(n)
        n = permute(o,i)
        i += 1
    return total

def prob44(n):
    """Pentagonal numbers are generated by the formula, Pn=n(3n-1)/2. The first ten pentagonal numbers are:

    1, 5, 12, 22, 35, 51, 70, 92, 117, 145, ...

    It can be seen that P4 + P7 = 22 + 70 = 92 = P8. However, their difference, 70  22 = 48, is not pentagonal.

    Find the pair of pentagonal numbers, Pj and Pk, for which their sum and difference is pentagonal and D = |Pk - Pj| is minimised; what is the value of D?"""
    pen = lambda x: x*(3*x-1)/2
    pl = dict([(pen(x),x) for x in range(1,n)])
    for p in pl:
        for q in pl:
            if (p+q) in pl and abs(p-q) in pl:
                print p,q
                return abs(p-q)
    return -1

def prob45(n):
    """After 40755, what is the next triangle number that is also pentagonal and hexagonal?"""
    tri = lambda x: x*(x+1)/2
    pen = lambda x: x*(3*x-1)/2
    hex = lambda x: x*(2*x-1)
    pl = []
    hl = []
    for i in range(300,n):
        t = tri(i)
        if t in pl and t in hl:
            return t
        else:
            pl.append(pen(i))
            hl.append(hex(i))

def prob46(n=6000):
    """What is the smallest odd composite that cannot be written as the sum of a prime and twice a square?"""
    primes = findPrimesTo(n)
    hashedprimes = dict([(x,1) for x in primes])
    oddcompo = lambda x: x%2 !=0 and not isPrime(x,primes)
    #composites = [x for x%2 != 0 and not isPrime(x) in range(3,n)]
    composites = filter(oddcompo, range(9,n))
    for c in composites:
        OK = False
        for q in range(1,(c/2)-2):
            sq = 2 * (q**2)
            if (c - sq) in hashedprimes:
                OK = True
                break
        if OK is False:
            print c,"can't be summed!"
            break
    return c


def prob47(n=150000):
    """Find the first four consecutive integers to have four distinct primes factors. What is the first of these numbers?"""
    cons = 0
    i = 11
    Q = 4
    primes = findPrimesTo(n)
    while cons < Q and i < n:

        L = primeFactors(i,primes)
        if len(L) >= Q:
            cons += 1
            #rint i," =",L
        else:
            #f cons > 0: print
            cons = 0
        i += 1
    return i - Q

def prob48(n=1000):
    """Find the last ten digits of 1**1 + 2**2 + ... + 1000**1000."""
    sum = 0
    for i in range(1, n+1):
        last10 = (i**i)
        sum += last10
    return sum % (10**10)

def prob49():
    """What 12-digit number do you form by concatenating the three 4-digit primes which are permutations of each other?"""
    primes = findPrimesTo(10000)
    f = [p for p in primes if p > 1000]
    l = len(f)
    for i in range(l):
        a = i2l(f[i])
        for j in range(i+1,l):
            b = i2l(f[j])
            if isPermutation(a,b):
                for k in range(j+1,l):
                    c = i2l(f[k])
                    if isPermutation(b,c):
                        A,B,C = l2i(a), l2i(b), l2i(c)
                        if (C-B) == (B-A):
                            aa,bb,cc = A,B,C
    return str(aa)+str(bb)+str(cc)


def prob50(n=1000000):
    """Which prime, below one-million, can be written as the sum of the most consecutive primes?"""
    primes = findPrimesTo(n)
    hashedprimes = dict([(x,1) for x in primes])
    i = 0
    LP = primes
    bestc = 0
    bestp = 0
    A = len(primes)
    for i in range(A):
        for j in range(i,A):
            S = sum(LP[i:j])
            if S > n:
                break
            if S in hashedprimes:
                if bestc < (j-i):
                    print "New best: ",S,"in",(j-i),"primes:"
                    print LP[i:j]
                    bestc = j-i
                    bestp = S
    print "BEST    ----->    ",bestp

def prob52(n=150000):
    """Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, contain the same digits."""
    for x in range(1,n):
        d = [getDigits(a*x) for a in range(1,7)]
        [b.sort() for b in d]
        if d.count(d[0]) == 6:
            return x
    return -1

def prob53(n=101):
    """How many, not necessarily distinct, values of  nCr, for 1<=n,<=100, are greater than one-million?"""
    facttable = dict([(x,factorial(x)) for x in range(0,n)])
    total = 0
    choose = lambda n,r: facttable[n] / (facttable[r] * facttable[n-r])
    for N in range(1,n):
        for R in range(0,N+1):
            if choose(N,R) > 1000000:
                total += 1
    return total

def prob55(n=10000):
    """If we take 47, reverse and add, 47 + 74 = 121, which is palindromic.

    Although no one has proved it yet, it is thought that some numbers, like 196, never produce a palindrome. A number that never forms a palindrome through the reverse and add process is called a Lychrel number. Due to the theoretical nature of these numbers, and for the purpose of this problem, we shall assume that a number is Lychrel until proven otherwise. In addition you are given that for every number below ten-thousand, it will either (i) become a palindrome in less than fifty iterations, or, (ii) no one, with all the computing power that exists, has managed so far to map it to a palindrome. In fact, 10677 is the first number to be shown to require over fifty iterations before producing a palindrome: 4668731596684224866951378664 (53 iterations, 28-digits).

    Surprisingly, there are palindromic numbers that are themselves Lychrel numbers; the first example is 4994.

    How many Lychrel numbers are there below ten-thousand?"""
    total = 0
    palind = lambda n: getDigits(n)[::-1]
    for i in range(1,n):
        iterations = 0
        q = i + l2i(palind(i))
        while iterations < 50 and q != l2i(palind(q)):
            iterations += 1
            q = q + l2i(palind(q))
        if iterations == 50:
            total += 1
    return total

def getDiagNums(list, i,jump,lim):
    if i >= lim:
        return list
    if isSquare(i):
        jump += 2
    list.append(i)
    return getDiagNums(list,i+jump,jump,lim)

def prob58(n):
    """What is the side length of the square spiral for which the ratio of primes along both diagonals first falls below 10%?"""
    ratio = 100.0
    i = 1
    t1 = time.time()
    primelist = dict([(x,'.') for x in findPrimesTo(n**2)])
    easyprimes = findPrimesTo(n)
    print "done generating primes in", time.time()-t1
    primes = 0
    #diagonals = [3,5,7]
    d = 1
    x = 1
    t2 = time.time()
    while ratio > 0.10:
        #print "_"
        d += 4
        i += 1
        #if i % 500 == 0:
        #    print i,ratio,time.time()-t2
        #    t2 = time.time()
        for p in range(3):
            x += i
            if x in primelist:
                #print ">",
                primes += 1
            elif isPrime(x,easyprimes):
                primes += 1
            #print x
        #print "sq.",
        x += i
        i += 1
        #print "(",x,")"
        ratio = (1.0 * primes) / d
    print "Total time:",time.time()-t1
    print i,"sides"
    print primes,"primes, /",d,"diagonals"
    print "Ratio:",ratio

def prob59(filename="cipher1.txt"):
    """XOR ciphering with 3-digit lowercase ASCII key."""
    import pickle
    newfile = file(filename)
    l = newfile.readlines()
    print l
    print "---------"
    l = [[int(n) for n in s.split(",")] for s in l]
    l = l[0]
    # Oh my god this code is so bad.
    for a in range(97,123):
        for b in range(97,123):
            for c in range(97,123):
                decipher = l[:]
                decipher[::3] = [d^a for d in decipher[::3]]
                decipher[1::3] = [d^b for d in decipher[1::3]]
                decipher[2::3] = [d^c for d in decipher[2::3]]
                finalstr = "".join([chr(x) for x in decipher])
                if finalstr.count("the") > 5:
                    print "Possible solution?"
                    print finalstr
                    print "(sum =", sum(decipher)


def prob62b(n=2500):
    """Find the smallest cube for which exactly five permutations of its digits are cube."""
    cubes = [x**3 for x in range(216,n)]
    l = len(cubes)
    for i in range(l):
        c = i2l(cubes[i])
        perms = 0
        #print cubes[i],
        for j in range(i+1,l):
            d = i2l(cubes[j])
            if len(c) != len(d):
                break
            if isPermutation(c,d):
                #print ".",
                perms += 1
        #print ""
        if perms == 4:
            return l2i(c)

def prob62(n,c):
    import sets
    for i in range(n):
        count = 0
        if i % 10 != 0:
            perms = all_perms(str(i**3))
            perms = list(sets.Set(perms))
            perms = [int(x) for x in perms]
            #print i,"-",i**3
            for p in perms:
                if isRoot(p,3):
                    #print p,"is a cube (",(p**(1.0/3)),"^3)"
                    count += 1
        if count > 1:
            print i,"-",count
        if count == c:
            return i

def isRoot(n,r):
    root = n**(1.0/r)
    rounded = round(root)
    return math.fabs(rounded-root) < 0.0000001

def prob63(n=21):
    """How many n-digit positive integers exist which are also an nth power?"""
    count = 0
    for i in range(1,10):
        for p in range(1,n+1):
            if len(i2l(i**p)) == p:
                count += 1
    return count

def prob68():
    """What is the maximum 16-digit string for a "magic" 5-gon ring?"""
    random.seed()
    possibles=[1,2,3,4,5,6,7,8,9,10]
    vars = [0,0,0,0,0,0,0,0,0,0]
    highestI=0
    cool=0
    highestL = []
    while cool < 10:
        poss = [p for p in possibles]
        tvars = [v for v in vars]
        while len(poss)>0:
            x = random.choice(poss)
            tvars[len(poss)-1] = x
            poss.remove(x)
        g1 = [tvars[0],tvars[1],tvars[2]] #g1=[a,b,c]
        g2 = [tvars[3],tvars[2],tvars[4]] #g2=[d,c,e]
        g3 = [tvars[5],tvars[4],tvars[6]] #g3=[f,e,g]
        g4 = [tvars[7],tvars[6],tvars[8]] #g4=[h,g,i]
        g5 = [tvars[9],tvars[8],tvars[1]] #g5=[j,i,b]
        if sum(g1) == sum(g2) == sum(g3) == sum(g4) == sum(g5):
            cool += 1
            outside = tvars[0]+tvars[3]+tvars[5]+tvars[7]+tvars[9]
            if outside > highestI:
                highestI = outside
                highestL = [d for d in tvars]
    return highestL

def prob69(n=1000000):
    """Find the value of n  1,000,000 for which n/ totient(n) is a maximum."""
    primes = findPrimesTo(n)
    bestx = 0
    bestv = 0.0
    for x in xrange(2,n+1):
        val = (1.0 * x) / totient(x,[],primes)
        if val > bestv:
            print x,val
            bestx = x
            bestv = val
    print bestx

def prob70(n=10**7):
    """Find the value of 1 < n < 10**7 for which totient(n) is a permutation of n and the ratio n/totient(n) produces a minimum."""
    primes = findPrimesTo(n)
    bestratio = 100
    bestX = 0
    for x in xrange(2,n):
        val = totient(x,[],primes)
        if val > floor(val) + 0.5:
            val += 1
        Dval = getDigits(int(val))
        Dx = getDigits(int(x))
        if len(Dval) == len(Dx):
            if isPermutation(Dval,Dx):
                R = x / val
                if R < bestratio:
                    bestratio = R
                    bestX = x
                    f = open('euler70results.txt', 'r+')
                    s= "! "+str(x)+"\t"+str(val)+"\t"+str(R)
                    f.write(s)
                    f.write("\n")
                    f.close()
                    print s
                    #print "\t",Dx,Dval
    return bestX


def prob72(n=1000000, q=500):
    """Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a reduced proper fraction.

How many elements would be contained in the set of reduced proper fractions for d  1,000,000?"""
    primes = findPrimesTo(n)
    dprimes = dict([(x,1) for x in primes])
    total = 0
    i = 2
    print "go"
    for d in xrange(2, n+1):
        if d in dprimes:
            total += d-1
        else:
            pfactors = primeFactors(d,primes)
            #print d,"\t",pfactors
            T = totient(d, pfactors, primes)
            #print d,T
            total += T
        if i == 10000:
            print ">",d
            i = 0
        i += 1
    return total

def prob74(n=1000000):
    """Create a chain by summing the factorials of a number's digits.
    How many chains, with a starting number below one million, contain exactly sixty non-repeating terms?"""
    chain = {1:1, 145:1, 169:3, 363601:3, 1454:3, 45361:2, 45362:2, 871:2, 872:2}
    ft = [factorial(x) for x in range(10)]
    fd = lambda x: sum(map(ft.__getitem__, i2l(x)))
    total = 0
    for a in range(1,n):
        x = a
        l = 0
        temp = []
        while x not in chain:
            temp += [x]
            tx = x
            l += 1
            x = fd(x)
            if x == tx:
                chain[x] = 1
        q = chain[x]
        for item in temp:
            chain[item] = q + l
            l -= 1
        if chain[a] == 60:
            print a
            total += 1
    return total



def laaa():
    sts = 10
    hop = 4
    for i in range(7, 101):
        sts += hop
        print i,sts
        hop += 2

def p76split(N,n):
    #print (6-N)*"\t",N,n
    if N == 1:
        if N >= n:
            return 1
        return 0
    #if n == 1:
    #   return 1
    if n > 1:
        return p76split(N-1,n+1) + p76split(n,0)
    if N > 1:
        return 1 + p76split(N-1,n+1)

def prob76(n):
    # This is probably going to be a disaster.
    # Is this finally a conundrum that CAN'T be solved with helicopter theft?
    print p76split(n,0)


def prob80(N):
    """Calculating the digital sum of the decimal digits of irrational square roots."""
    decimal.getcontext().prec = 105
    sum = 0
    for i in range(2,N):
        if not isSquare(i):
            f = decimal.Decimal.sqrt(decimal.Decimal(i))
            s = str(f)
            part = 0
            for n in s[:101]:
                if n != ".":
                    n = int(n)
                    part += n
            sum += part
    return sum

def prob92(n=10000000):
    """A number chain is created by continuously adding the square of the digits in a number to form a new number until it has been seen before.
    Any chain that arrives at 1 or 89 will become stuck in an endless loop. What is most amazing is that EVERY starting number will eventually arrive at 1 or 89.
    How many starting numbers below ten million will arrive at 89?"""
    sq = [x**2 for x in range(10)]
    digisum = lambda x: sum([sq[d] for d in getDigits(x)])
    results = {1:1, 89:89}
    for i in range(1,568):
        #print "----------------"
        R = digisum(i)
        #print i,"->",R,
        if R not in results:
            Q = [i]
            while R != 1 and R != 89 :
                Q += [R]
                R = digisum(R)
                #print "->",R,
                if R in results:
                    R = results[R]
                    break
            #print
            for t in Q:
                #print "\tresults[",t,"]=",R
                results[t] = R
        else:
            results[i] = results[R]
    print results
    t1 = time.time()
    is89 = 0
    for i in xrange(1,n):
        R = digisum(i)
        if results[R] == 89:
            is89 += 1
    print time.time() - t1
    return is89

def prob94(n=1000000000):
    """It is easily proved that no equilateral triangle exists with integral length sides and integral area. However, the almost equilateral triangle 5-5-6 has an area of 12 square units.
    We shall define an almost equilateral triangle to be a triangle for which two sides are equal and the third differs by no more than one unit.
    Find the sum of the perimeters of all almost equilateral triangles with integral side lengths and area and whose perimeters do not exceed one billion (1,000,000,000)."""
    S = lambda s,a,b: sqrt(s*(s-a)*(s-a)*(s-b))
    #isint = lambda x: abs(x - x//1) < 0.00001
    isint = lambda x: int(x) == x
    total = 0
    i = 1
    for a in xrange(2,n/3):
        ok = False
        b1,b2 = a-1, a+1
        s1,s2 = a + (b1/2.0), a + (b2/2.0)
        S1,S2 = S(s1,a,b1), S(s2,a,b2)
        if isint(S1):
            p = 2*a + b1
            if p <= n:
                total += p
                ok = True
        if isint(S2):
            p = 2*a + b2
            if p <= n:
                total += p
                ok = True
        if ok == True:
            if i == 1000000:
                print a,p
                i = 0
            i += 1
    return total


def prob97():
    """Find the last ten digits of the non-Mersenne prime:  28433x2**7830457 + 1"""
    n = ((28433 * (2**7830457))+1) % 10000000000
    return n

def prob99():
    """Which base/exponent pair in the file has the greatest numerical value?"""
    import pickle
    newfile = file("base_exp.txt")
    l = newfile.readlines()
    l = [[long(n) for n in s.split(",")] for s in l]
    ll = [((log(n[0]))*((n[1]))) for n in l]
    lrg = 0
    lrgi = 0
    largest = 0
    li = 0
    i = 1
    for x in ll:
        if x > largest:
            largest = x
            li = i
        i += 1
    return li

def probBB(blues,total):
    return float(blues**2 - blues) / float(total**2 - total)

def prob100(n):  # HOPELESS.
    maxchips = 10L**14L
    half = float(1)/float(2)
    print half
    chips = long(n) + 1L
    print chips
    while chips < maxchips:
        print chips,
        blues = chips/2L
        F = 0
        while blues < chips:
            blues = float(blues)
            if F == 100000:
                print ".",
                F = 0
            chips = float(chips)
            prob = probBB(blues, chips)
            if prob > half:
                blues = chips + 1L 
            if prob == half:
                print "yay!  %d blue chips in %d total chips!" % (blues,chips)
                return blues
            blues += 1L
            F += 1
        print
        chips += 1L


def prob102(filename="triangles.txt"):
    """Using triangles.txt, a 27K text file containing the co-ordinates of one thousand "random" triangles, find the number of triangles for which the interior contains the origin."""

    def p102area(A,B,C):
        """Computes area through cross-products"""
        x1,y1 = A
        x2,y2 = B
        x3,y3 = C
        area = (abs(x1*y2+x2*y3+x3*y1 - x1*y3-x3*y2-x2*y1)) / 2.0
        return area

    import pickle
    l = file(filename).readlines()
    l = [[int(x) for x in s.split(",")] for s in l]
    #print l
    i = 0
    O = [0,0]
    EPSILON = 0.01
    for set in l:
        A = set[0:2]
        B = set[2:4]
        C = set[4:6]
        if (abs(p102area(A,B,C) - (p102area(A,B,O) + p102area(B,O,C) + p102area(O,A,C))) < EPSILON):
            i += 1
    return i



def prob112(n=0.99):
    """Working from left-to-right if no digit is exceeded by the digit to its left it is called an increasing number; for example, 134468.
Similarly if no digit is exceeded by the digit to its right it is called a decreasing number; for example, 66420.
We shall call a positive integer that is neither increasing nor decreasing a "bouncy" number; for example, 155349.
Find the least number for which the proportion of bouncy numbers is exactly 99%."""
    bouncy = 0
    for i in itertools.count(100):
        D = getDigits(i)
        x = D[0]
        y = D[1]
        direction = x-y
        for b in range(2,len(D)):
            b = D[b]
            if direction == 0:
                direction = y-b
                y = b
            elif direction > 0 and y-b < 0:
                bouncy += 1
                break
            elif direction < 0 and y-b > 0:
                bouncy += 1
                break
            else:
                y = b
        if (1.0 * bouncy) / i >= n:
            break
    return i

def prob113(n=10**100):
    """How many numbers below a googol (10100) are not bouncy?"""
    # haha fuck this.
    notbouncy = 99
    for i in itertools.count(100):
        if i >= n:
            break
        D = getDigits(i)
        x = D[0]
        y = D[1]
        direction = x-y
        bouncy = False
        for b in range(2, len(D)):
            b = D[b]
            if direction == 0:
                direction = y-b
                y = b
            elif direction > 0 and y-b < 0:
                bouncy = True
                break
            elif direction < 0 and y-b > 0:
                bouncy = True
                break
            else:
                y = b
        if not bouncy:
            notbouncy += 1
    return notbouncy

def prob119(n=30, p=70, q=20):
    """The number 512 is interesting because it is equal to the sum of its digits raised to some power: 5 + 1 + 2 = 8, and 8^3 = 512. Another example of a number with this property is 614656 = 284.
    We shall define an to be the nth term of this sequence and insist that a number must contain at least two digits to have a sum.
    You are given that a2 = 512 and a10 = 614656.
    Find a30."""
    d = {}
    for N in range(2,p+1):
        for P in range(2,q+1):
            d[N**P] = [N,P]
    l = []
    for k,v in d.items():
        if sumDigits(k) == v[0]:
            l.append([k,v])
    l.sort()
    return l[n-2] # for some reason 2401 isn't included??? whatever

def prob124(n=100000, k=10000):
    """The radical of n, rad(n), is the product of distinct prime factors of n.
    Let E(k) be the kth element in the sorted n column; for example, E(4) = 8 and E(6) = 9.

If rad(n) is sorted for 1 <= n <= 100000, find E(10000)."""
    primes = findPrimesTo(n+1)
    from operator import mul
    rad = lambda x,factors: reduce(mul,factors,1)
    l = [[rad(x, primeFactors(x,primes)), x] for x in range(1,n+1)]
    l.sort()
    return l[k-1][1]

def prob127(n=120000):
    """The radical of n, rad(n), is the product of distinct prime factors of n.
    We shall define the triplet of positive integers (a, b, c) to be an abc-hit if:
        1.  GCD(a, b) = GCD(a, c) = GCD(b, c) = 1
        2.  a < b
        3.  a + b = c
        4.  rad(a*b*c) < c
    Find sum(c) for c<120000."""
    primes = findPrimesTo(n)
    dprimes = dict([(x,1) for x in primes])
    from operator import mul
    rad = lambda factors: reduce(mul,factors,1)
    total = 0
    i = 0
    C = [c for c in range(3,n) if c not in dprimes]
    F = dict([(x, dict( [(f,1) for f in primeFactors(x,primes)] ) ) for x in range(n)])
    def mutex(a,b):
        for k in F[a]:
            if k in F[b]:
                return False
        return True
    print "let's do this."
    maxx = 0
    for c in C:
        B = [b for b in range((c//2)+1,c) if b not in dprimes and mutex(b,c)]
        for b in B:
            a = c-b
            if mutex(a,b) and mutex(a,c):
                if rad(F[a].keys() + F[b].keys() + F[c].keys()) < c:
                    i += 1
                    print i,"\t",a,b,c
                    total += c
    return total

def prob142(n=100):
    """Find the smallest x + y + z with integers x > y > z > 0 such that x + y, x - y, x + z, x - z, y + z, y - z are all perfect squares."""
    sq = dict([(x**2,x) for x in range(1,n)])
    L = n**2
    i = 0
    for x in xrange(3,L):
        if i == 1000:
            print x
            i = 0
        i += 1
        for y in xrange(2,x):
            if (x+y) in sq and (x-y) in sq:
                for z in xrange(1,y):
                    if (x+z) in sq and (x-z) in sq and (y+z) in sq and (y-z) in sq:
                        print (x+y),(x-y),(x+z),(x-z),(y+z),(y-z)
                        return x,y,z
    return "balls"

def digitsAreOdd(n):
    m = n
    while m > 0:
        d = m%10
        if d == 0 or d%2 == 0:
            return False
        m = m/10
    return True

def prob145(n):
    """How many reversible numbers are there below one billion?"""
    count = 0
    f = 1
    t1 = time.time()
    q = 1
    for i in itertools.count(1):
        q += 1
        if i > n:
            break
        if q > 100000:
            print ".",
            q = 1
        if i % 10 != 0:
            ii = reverseDigits(i)
            r = i + ii
            if digitsAreOdd(r):
                f += 1
                if f > 100:
                    print i
                    f = 1
                    q = 1
                count += 1
    print time.time()-t1,"s"
    return count

def prob179(N=10**7):
    """Find the number of integers n < 10^7 for which n and n+1 have the
    same number of divisors."""
    count = 0
    p = 0
    #divisors = [len(gimmeDivisors(e)) for e in range(2,(sqrt(N)+1))]
    nplusdc = findDivisors(2)
    for n in range(2,N):
        ndc = nplusdc
        nplusdc = findDivisors(n+1)
        #ndc = divisors[n]
        #nplusdc = divisors[n+1]
        if (ndc == nplusdc):
            count += 1
            p += 1
            if (p == 1000):
                print n
                p = 0
    return count

def numPrimeFactors(n, primes):
    l = 0
    for i in primes:
        while i<=n and n%i == 0:
            if l > 2:
                return l
            l += 1
            n = n/i
    return l

def prob187(n=10**8):
    """ How many composite integers, n < 10**8, have precisely two,
        not necessarily distinct, prime factors?"""
    print "generating primes..."
    primes = findPrimesTo(n/2+1)
    total = 0
    l = len(primes)
    print "ok"
    for i in xrange(l):
        a = primes[i]
        for j in xrange(i,l):
            b = primes[j]
            if a*b > n:
                break
            else:
                total += 1
    return total

def prob188(x=1777,y=1855,n=9):
    """Calculate the last 8 digits of 1777 (up arrow)(up arrow) 1855."""
    base = x
    tet = y
    if tet <= n:
        print "BAD RESULTS, KILL ME"
    modlim = 10 ** n
    total = base
    for i in range(0,n):
        print total, ":"

        print "Now performing ",base,"^",total," % ",modlim
        # Replace big exponentiation with repeated multiplication
        # with modulus built in!
        temp = base
        #print "\t",base,"^",total,":"
        for j in range(1,total):
            #print "\t\t",temp," * ",base," = ",
            temp = (temp * base)
            temp = temp % (100*modlim)
            #print temp
        total = temp % modlim
        #total = ((base**total) % (10**(n)))
        print "-->",total
    print "\n!~", (total % modlim)

def prob191(n):
    """Prize strings"""
    t1 = time.time()

    print time.time()-t1

def prob197(n=10**12):
    """Investigating the behavior of a recursively defined sequence."""
    f = (lambda x: (floor(2**(30.403243784-(x**2))) * 10**-9))
    u = -1
    W = 0
    countr = n//20
    for i in itertools.count():
        if W >= countr:
            print i
            W = 0
        if i > n:
            break
        u = f(u)
        W += 1
    v = f(u)
    print '%.9f' % (u+v)

def p206mask(n, mask):
    nlist = list(str(n))
    i = 1
    for digit in nlist:
        if i%2 == 1 and digit != mask[(i-1)/2]:
            return False
        i += 1
    return True

def prob206():
    """Find the unique positive integer whose square has the form
    1x2x3x4x5x6x7x8x9x0, where each x is a single digit."""

    n = 1010101010
    mask = ['1','2','3','4','5','6','7','8','9','0']
    x = 0
    while p206mask(n**2,mask) is False:
        if x > 100000:
            print n
            x = 1
        n += 10
        if n > 1389026623:
            return "shit."
        x += 1
    return n

def prob214(n=40000000, L=25):
    """By iterating the totient function, each positive integer generates a decreasing chain of numbers ending in 1.
    What is the sum of all primes less than 40000000 which generate a chain of length 25?"""
    primes = findPrimesTo(n+1)
    chain = {1:1}
    total = 0
    Q = 0
    for i in primes:
        chainl = 1
        x = i-1
        tmp = {}
        #print x,":\n\t",
        while x not in chain:
            tmp[x] = -1 * chainl
            chainl += 1
            x = int(totient(x, [], primes) + 0.05)
            #print x,
        chainl += chain[x]
        for t in tmp:
            if t not in chain:
                chain[t] = tmp[t] + chainl
                #print "(added chain[",t,"] as ",chain[t],")"
        #if i not in chain:
        #    chain[i] = chainl
        #if i-1 not in chain:
        #    chain[i-1] = chainl-1
        #print i,chainl
        if Q == 10000:
            print i,"..."
            Q = 0
        Q += 1
        #print i,"\ttotal chain length:",chainl,"\t(chain[",x,"] =",chain[x],")"
        if chainl == L:
            print i,"!!!"
            Q = 0
            #Qi = 1
            #while Q != 1:
            #    print "\t",Qi,". ",Q,
            #    if Q in chain:
            #        print "{",chain[Q],"}, should be",L-Qi,"?}",
            #    print ""
            #    Q = int(totient(Q,[],primes))
            #    Qi += 1
            #print "\t",Qi,". ",Q,"\nthe end."
            total += i
    #print chain
    return total


def p216test(n,q=100):
    primes = findPrimesTo(q)
    t = lambda x: (2*(x**2))-1
    t1 = time.time()
    total = 0
    ptotal = 0
    for i in xrange(2,n+1):
        w = t(i)
        if isPrime(w, primes):
            total += 1
            if isPrime(i, primes):
                ptotal += 1
    print total,time.time()-t1
    print "(",ptotal,"n's were prime)"
    t1 = time.time()
    total = reduce( lambda x,y: x+isPrime(y,primes) , [t(x) for x in xrange(2,n+1)] )
    print total-6,time.time()-t1


def prob216(n=50000000, q=100):
    """How many numbers of the form t(n) = 2*(n^2) - 1 are prime for
    n <= 50,000,000?"""

    t = lambda x: (2 * (x**2)) - 1
    primelist = findPrimesTo(q)
    total = 0
    gooddivisors = {}
    T = time.time()
    for i in xrange(2,n+1):
        w = t(i)
        if isPrime(w, primelist):
            print i
            total += 1
    print "total time: ",time.time()-T
    return total

def prob234(n=999966663333):
    """For an integer n >= 4, we define the lower prime square root of n, denoted by lps(n), as the largest prime <= sqrt(n) and the upper prime square root of n, ups(n), as the smallest prime>= sqrt(n).
    Let us call an integer n >= 4 semidivisible if one of lps(n) and ups(n) divides n, but not both.
    The sum of the 92 semidivisible numbers up to 1000 is 34825.  What is the sum of all semidivisible numbers not exceeding 999966663333 ?"""
    primes = findPrimesTo(sqrt(n)+1000)
    total = 0
    count = 0
    lps = 0 # primes[0] = 2
    ups = 0
    for i in xrange(4,n+1):
        S = sqrt(i)
        if primes[lps+1] <= S:
            lps += 1
        L = primes[lps]
        if primes[ups] < S:
            ups += 1
        R = primes[ups]
        if (i%L == 0) is not (i%R == 0):
            total+=i
            if count == 10000:
                print i
                count = 0
            count+=1
            #print count,L**2,"<=",i,"<=",R**2
            #print "\t",i,"%",L,"=",(i%L),", ",i,"%",R,"=",(i%R)
        """
        if primes[lps+1]**2 <= i:
            lps += 1
        L = primes[lps]**2
        if primes[ups]**2 < i:
            ups += 1
        R = primes[ups]**2
        if i%L is not i%R:
            total += i
            count += 1
        """
    return total


def prob235(low=1.002,high=1.003):
    """Given is the arithmetic-geometric sequence u(k) = (900-3k)r^(k-1).
    Let s(n) = sum of k 1..n u(k).
    Find the value of r for which s(5000) = -600,000,000,000."""
    n = 5000
    r = (low + high) / 2.0

    u = lambda k: (900-(3*k))*(r**(k-1))
    s = lambda n: sum(u(k) for k in xrange(1,n+1))

    sol = s(n)
    EPSILON = 0.5
    goal = -600000000000
    while abs(sol-goal) > EPSILON:
        if sol < goal:
            high = r
        else:
            low = r
        r = (low + high) / 2.0
        sol = s(n)
    print "s(%d) = %.15f" % (n, sol)
    print "r = %.15f" % (r)
    return r

def prob243(n=1000000, step=30030, ratio=(15499.0/94744)):
    """A positive fraction whose numerator is less than its denominator is
    called a proper fraction.  For any denominator d, there will be d-1 proper
    fractions.  We shall call a fraction that cannot be cancelled down a
    resilient fraction.
    Furthermore we shall define the resilience of a denominator, R(d), to be
    the ratio of its proper fractions that are resilient; for example, R(12)=4/11.
    In fact, d=12 is the smallest denominator having a resilience R(d) < 4/10.
    Find the smallest denominator d having a resilience R(d) < 15499/94744."""
    primes = findPrimesTo(n)
    dprimes = dict([(x,1) for x in primes])
    total = 0
    bestratio = 1
    i = 2
    print "go"
    d = 0
    while True:
        d += step
        if d not in dprimes:
            if d > n:
                if isPrime(d, primes):
                    primes += [d]
            pfactors = primeFactors(d,primes)
            T = totient(d, pfactors, primes)
            dratio = T / (d-1.0)
            if dratio < ratio:
                return d
            elif dratio < bestratio:
                print "new best ratio:",d,dratio
                bestratio = dratio
    return "crap"

def prob245(n=2*(10**11)):
    """We further define the coresilience of a number n  1 as C(n) = (n - totient(n)) / (n - 1)  .
The coresilience of a prime p is C(p) = 1 / (p - 1) .

Find the sum of all composite integers 1 < n <= 10**11, for which C(n) is a unit fraction."""
    primes = findPrimesTo(50000)
    coresil = lambda x,f: (x - totient(x,f,primes)) / (x-1)
    isUnit = lambda x: abs(x - x//1) < 0.00001
    total = 0
    for i in xrange(3,n+1,2):
        if not isPrime(i, primes):
            #print i,
            factors = primeFactors(i,primes)
            C = coresil(i,factors)
            #print C,
            C = C ** -1
            #print C
            if isUnit(C):
                print i,"\t",factors,C
                total += i
    return total


def prob248(n=150000):
    """Find the 150,000th number for which euler's totient function = 13!"""
    solution = 6227020800
    A = 6227180929
    i = 0
    x = A
    p = findPrimesTo(A/1000)
    easy = p[:500]
    print "done primes"
    out = 0
    while i < n:
    #for x in itertools.count(A):
        if not isPrime(x,easy):
        #    p += [x]
        #else:
            factors = primeFactors(x,p)
            t = totient(x,factors,p)
            if t == solution:
                i += 1
                out=0
                print "Solution #",i,": ",x,factors
        x += 1
        out += 1
        if out == 1000:
            print "currently at",x
            out =0
    return x

if __name__ == "__main__":
    print prob26(1000)