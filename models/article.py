# -*- coding: utf-8 -*-
import lxml.html
from lxml.html import soupparser
from lxml import etree
from copy import deepcopy
from goose.text import innerTrim
from goose.text import encodeValue



class Article(object):

    def __init__(self, url, raw_html):
        # title of the article
        self.title = None

        self.cleaned_text = u""
        self.meta_description = u""
        self.meta_lang = u""
        self.meta_favicon = u""
        self.meta_keywords = u""
        self.canonical_link = u""
        self.domain = u""
        self.top_node = None
        self.tags = set()
        self.final_url = url
        self.link_hash = ""
        self.raw_html = raw_html
        self.doc = None
        self.raw_doc = raw_html
        self.publish_date = None
        self.additional_data = {}
