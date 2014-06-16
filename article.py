from page import Page

class Article(Page):
    def __init__(self):
        Page.__init__(self)
        self.type = "article"
        self.title = None

        # stores the lovely, pure text from the article,
        # stripped of html, formatting, etc...
        # just raw text with paragraphs separated by newlines.
        # This is probably what you want to use.
        self.cleaned_text = u""

        # meta description field in HTML source
        self.meta_description = u""

        # meta lang field in HTML source
        self.meta_lang = u""

        # meta favicon field in HTML source
        self.meta_favicon = u""

        # meta keywords field in the HTML source
        self.meta_keywords = u""

        # The canonical link of this article if found in the meta data
        self.canonical_link = u""

        # holds the domain of this article we're parsing
        self.domain = u""

        # holds the top Element we think
        # is a candidate for the main body of the article
        self.top_node = None

        # holds a set of tags that may have
        # been in the artcle, these are not meta keywords
        self.tags = set()
        # stores the final URL that we're going to try
        # and fetch content against, this would be expanded if any
        self.final_url = u""
        # stores the MD5 hash of the url
        # to use for various identification tasks
        self.link_hash = ""
        # stores the RAW HTML
        # straight from the network connection
        #Already in page
        #self.raw_html = u""
        
        # the lxml Document object
        self.doc = None
        # this is the original JSoup document that contains
        # a pure object from the original HTML without any cleaning
        # options done on it
        self.raw_doc = None
        # Sometimes useful to try and know when
        # the publish date of an article was
        self.publish_date = None

        # A property bucket for consumers of goose to store custom data extractions.
        self.additional_data = {}
        self.links = None
        self.outlinks = None
        self.backlinks = None
        self.start_date = today()
        
        # parser
        self.parser = get_parser()
        
        # init the extractor
        self.extractor = self.get_extractor()

        # init the document cleaner
        self.cleaner = self.get_cleaner()

        # init the output formatter
        self.formatter = self.get_formatter()

    def extract(self):
        self.link_hash = '%s.%s' % (hashlib.md5(self.raw_html).hexdigest(), time.time())

        
        if self.raw_html is None or self.raw_html == '':
            return self.article

        # create document
        self.doc = self.get_document()

        # article
        self.final_url = self.url
        self.link_hash = self.link_hash
        self.raw_doc = deepcopy(self.doc)
        
        #article values
        self.title = self.extractor.get_title()
        self.meta_lang = self.extractor.get_meta_lang()
        self.meta_favicon = self.extractor.get_favicon()
        self.meta_description = self.extractor.get_meta_description()
        self.meta_keywords = self.extractor.get_meta_keywords()
        self.canonical_link = self.extractor.get_canonical_link()
        self.domain = self.extractor.get_domain()
        self.tags = self.extractor.extract_tags()
        
        #links
        self.links = self.extractor.extract_links()
        self.outlinks = self.extractor.extract_outlinks()
        self.backlinks = self.extractor.extract_backlinks()
        # before we do any calcs on the body itself let's clean up the document
        self.doc = self.cleaner.clean()

        # big stuff
        self.top_node = self.extractor.calculate_best_node()

        # if we have a top node
        # let's process it
        if self.top_node is not None:
            # post cleanup
            self.top_node = self.extractor.post_cleanup()

            # clean_text
            self.cleaned_text = self.formatter.get_formatted_text()
            return self
    
    def get_formatter(self):
        return StandardOutputFormatter(self.article)

    def get_cleaner(self):
        return StandardDocumentCleaner(self.article)

    def get_document(self):
        self.doc = self.parser.fromstring(self.raw_html)
        return self.doc

    def get_extractor(self):
        return StandardContentExtractor(self.article)
    

    def filter(self):
        #to
        '''Bool Decide if page is relevant and match the correct query. Reformat the query properly: supports AND, OR and space'''
        if self.article.cleaned_text is not None or self.article.cleaned_text != '':
            self.query = re.sub('-', ' ', self.query) 
            if 'OR' in self.query:
                for each in self.query.split('OR'):
                    query4re = each.lower().replace(' ', '.*')
                    if re.search(query4re, self.article.cleaned_text, re.IGNORECASE) or re.search(query4re, self.url, re.IGNORECASE):
                        return True

            elif 'AND' in self.query:
                query4re = self.query.lower().replace(' AND ', '.*').replace(' ', '.*')
                return bool(re.search(query4re, self.article.cleaned_text, re.IGNORECASE) or re.search(query4re, self.url, re.IGNORECASE))
            #here add NOT operator
            else:
                query4re = self.query.lower().replace(' ', '.*')
                return bool(re.search(query4re, self.article.cleaned_text, re.IGNORECASE) or re.search(query4re, self.url, re.IGNORECASE))
        else:
            return False        
