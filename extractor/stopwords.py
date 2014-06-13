# -*- coding: utf-8 -*-

import os
import re
import string

class WordStats(object):

    def __init__(self):
        # total number of stopwords or
        # good words that we can calculate
        self.stop_word_count = 0

        # total number of words on a node
        self.word_count = 0

        # holds an actual list
        # of the stop words we found
        self.stop_words = []

    def get_stop_words(self):
        return self.stop_words

    def set_stop_words(self, words):
        self.stop_words = words

    def get_stopword_count(self):
        return self.stop_word_count

    def set_stopword_count(self, wordcount):
        self.stop_word_count = wordcount

    def get_word_count(self):
        return self.word_count

    def set_word_count(self, cnt):
        self.word_count = cnt
        
class StopWords(object):

    PUNCTUATION = re.compile("[^\\p{Ll}\\p{Lu}\\p{Lt}\\p{Lo}\\p{Nd}\\p{Pc}\\s]")
    TRANS_TABLE = string.maketrans('', '')
    _cached_stop_words = {}

    def __init__(self, language='en'):
        # TODO replace 'x' with class
        # to generate dynamic path for file to load
        if not language in self._cached_stop_words:
            path = os.path.join('utils', 'stopwords-%s.txt' % language)
            self._cached_stop_words[language] = set(FileHelper.loadResourceFile(path).splitlines())
        self.STOP_WORDS = self._cached_stop_words[language]

    def remove_punctuation(self, content):
        # code taken form
        # http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
        if isinstance(content, unicode):
            content = content.encode('utf-8')
        return content.translate(self.TRANS_TABLE, string.punctuation)

    def candidate_words(self, stripped_input):
        return stripped_input.split(' ')

    def get_stopword_count(self, content):
        if not content:
            return WordStats()
        ws = WordStats()
        stripped_input = self.remove_punctuation(content)
        candidate_words = self.candidate_words(stripped_input)
        overlapping_stopwords = []
        c = 0
        for w in candiate_words:
            c += 1
            if w.lower() in self.STOP_WORDS:
                overlapping_stopwords.append(w.lower())

        ws.set_word_count(c)
        ws.set_stopword_count(len(overlapping_stopwords))
        ws.set_stop_words(overlapping_stopwords)
        return ws
