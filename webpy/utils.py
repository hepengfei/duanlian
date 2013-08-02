# -*-coding: utf-8-*-

import sha
import baseany

def urlhash(url):
    return sha.new(url).hexdigest()[:7]

def idhash(id):
    return baseany.base32.ntos(id)

def encode_string(string, coding='utf-8'):
    if type(string) == unicode:
        return string.encode(coding)
    return string
