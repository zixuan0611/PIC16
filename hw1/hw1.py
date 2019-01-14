import math
import random
from copy import deepcopy


# Input: a list c of numbers
# Return: a new list k, such that k[i]=1 if c[i]>i, k[i] = 0 if c[i]=i, k[i] = -1 if c[i]<i
def largerIndex(c):
    k = []  # create the return list k
    for i in range(len(c)):  # iterate through the input list
        if c[i] > i:
            k.append(1)
        elif c[i] == i:
            k.append(0)
        elif c[i] < i:
            k.append(-1)

    return k


# Input: a positive integer n
# Return: a list of all the square numbers up to (and possibly including) n
def squareUpTo(n):
    result = []  # create the return list l
    for i in range(n+1):
        r = math.sqrt(i)
        if (r - int(r)) == 0:  # check if the number is a square number by testing if the square root is an integer
            result.append(i)

    return result


# a function uses only fair coins to generate a biased coin with success probability 1/3
def flip1in3():
    # flip the fair coin twice
    c1 = random.randint(0, 1)
    c2 = random.randint(0, 1)

    if (c1 + c2) == 0:  # try again on TT
        return flip1in3()
    elif (c1 + c2) == 2:  # report success on HH
        print ('success')
        return True
    else:  # report failure on HT or TH
        print ('failure')
        return False


# Input: a list c of integers. elements appear either twice or once
# Return: a list of elements that appear twice
def duplicates(c):
    t = []  # create the output list
    for i in range(len(c)):  # iterate through the input list
        a = c[i]
        for j in range(i+1, len(c)):
            b = c[j]
            if a == b:  # find elements that appear twice
                t.append(a)

    return t


# Input: a dictionary d
# Return: the length of a longest path found in the dictionary
def longestpath(d):
    path = 0
    longest = 0
    for key in d:
        d_copy = deepcopy(d)  # we make a deep copy of d to avoid infinite loop
        while key in d_copy:   # find a path length for a key in the dictionary
            m = key
            key = d[key]
            path = path + 1
            del d_copy[m]
        if path > longest:     # compare the path length for one key from the previously found longest path
            longest = path
        path = 0

    return longest
