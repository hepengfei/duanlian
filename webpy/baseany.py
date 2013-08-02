# -*-mode:python; coding:utf-8-*-

import math

# 只支持正整数

IDX_BASE = 0
IDX_ITOA = 1
IDX_ATOI = 2

__debug = False

def new_index(basemap):
    index=(len(basemap), basemap, {})
    for idx, char in enumerate(basemap):
        index[IDX_ATOI][char] = idx
    return index

def check_index(index):
    basen1=index[IDX_BASE]
    basen2=len(index[IDX_ITOA])
    basen3=len(index[IDX_ATOI].keys())
    return basen1 == basen2 and basen1 == basen3

def ntos(number, index):
    basen = index[IDX_BASE]
    if number == 0:
        return index[IDX_ITOA][0]
    string=''
    while number > 0:
        remainder = number % basen
        char = index[IDX_ITOA][remainder]
        string = char + string
        number = number / basen
        if __debug:
            print "%d %s %d %s" % (remainder, char, number, string)
    return string

def ston(string, index):
    basen=index[IDX_BASE]
    number=0
    reversed_string=string[::-1]
    for idx, char in enumerate(reversed_string):
        value = index[IDX_ATOI][char]
        number = number + value * int(math.pow(basen, idx))
        if __debug:
            print "%d %s %d" % (value, char, number)
    return number



    
class BaseAny:
    def __init__(self, basemap):
        self.__index = new_index(basemap)
        assert(check_index(self.__index))
    def ntos(self, number):
        return ntos(number, self.__index)
    def ston(self, string):
        return ston(string, self.__index)

# export factory method
def new(basemap):
    return BaseAny(basemap)

# predefine base<N>
base32map="abcdefghijkmnpqrstuvwxyz23456789"
base32 = new(base32map)




# test methods
def test_one(baseany, number):
    string = baseany.ntos(number)
    n2 = baseany.ston(string)
    assert(number == n2)

number_to_test = (0, 1, 9, 10, 42, 43, 51, 99, 255, 999, 1232, 3123, 323123, 1233123123, 3123133123,347887856457)

def test(baseany, number_array = number_to_test):
 for n in number_array:
     test_one(baseany, n)

if __name__ == '__main__':
    base9 = new('dfasljthz')
    test(base9)
    test(base32)
    print "All test passed."



