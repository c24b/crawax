# -*- coding: utf-8 -*-
#utils
import time
import hashlib
import re
import os
import string
import goose
import codecs
import urlparse


TABSSPACE = re.compile(r'[\s\t]+')


def innerTrim(value):
    if isinstance(value, (unicode, str)):
        # remove tab and white space
        value = re.sub(TABSSPACE, ' ', value)
        value = ''.join(value.splitlines())
        return value.strip()
    return ''


def encodeValue(value):
    string_org = value
    try:
        value = smart_unicode(value)
    except (UnicodeEncodeError):
        value = smart_str(value)
    except:
        value = string_org
    return value


class BuildURL(object):
    def __init__(self, url, finalurl=None):
        self.url = url
        self.finalurl = finalurl
        
    def getHostname(self, o):
        if o.hostname:
            return o.hotname
        elif self.finalurl:
            oo = urlparse(self.finalurl)
            if oo.hostname:
                return oo.hostname
        return None

    def getScheme(self, o):
        if o.scheme:
            return o.scheme
        elif self.finalurl:
            oo = urlparse(self.finalurl)
            if oo.scheme:
                return oo.scheme
        return 'http'

    def getUrl(self):
        url_obj = urlparse(self.url)
        scheme = self.getScheme(url_obj)
        hostname = self.getHostname(url_obj)

class StringSplitter(object):
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def split(self, string):
        if not string:
            return []
        return self.pattern.split(string)


class StringReplacement(object):

    def __init__(self, pattern, replaceWith):
        self.pattern = pattern
        self.replaceWith = replaceWith

    def replaceAll(self, string):
        if not string:
            return u''
        return string.replace(self.pattern, self.replaceWith)


class ReplaceSequence(object):

    def __init__(self):
        self.replacements = []

    #@classmethod
    def create(self, firstPattern, replaceWith=None):
        result = StringReplacement(firstPattern, replaceWith or u'')
        self.replacements.append(result)
        return self

    def append(self, pattern, replaceWith=None):
        return self.create(pattern, replaceWith)

    def replaceAll(self, string):
        if not string:
            return u''

        mutatedString = string

        for rp in self.replacements:
            mutatedString = rp.replaceAll(mutatedString)
        return mutatedString

def hash_content(url):
	raw_html = raw_html.encode('utf-8')
    link_hash = '%s.%s' % (hashlib.md5(raw_html).hexdigest(), time.time())
