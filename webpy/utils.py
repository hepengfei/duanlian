# -*-coding: utf-8-*-

import sha

def urlhash(url):
    return sha.new(url).hexdigest()[:7]

def encode_string(string, coding='utf-8'):
    if type(string) == unicode:
        return string.encode(coding)
    return string
