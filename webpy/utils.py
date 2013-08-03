# -*-coding: utf-8-*-

import sha
import config

def urlhash(url):
    return sha.new(url).hexdigest()[:7]

def idtostr(id):
    return config.BASE32.ntos(id)

def encode_string(string, coding='utf-8'):
    if type(string) == unicode:
        return string.encode(coding)
    return string

def check_url(url):
    return True
