
import unicodedata
import urllib
from bs4 import BeautifulSoup
import time
import hashlib
import os
import re
#import requests
import shutil

os.chdir('C:\Users\SVR\pages')
print(os.getcwd())

path = os.getcwd()
i = 1
d = {}
total_doc_length = []
for filename in os.listdir(path):
  
    #print(filename)
    soup = BeautifulSoup(open(filename))
    #print(soup.find('title'))
    #print(type(soup.get('title'))
    title = soup.title.string.encode('utf-8').lower()
    #print(title)
    
    #title_content = title.get('title')
    
    #body = soup.find('body')
    body = soup.find('body').text.encode('utf-8').lower()
    
    #print(whole_doc)
    #print(body)
    body1 = re.sub("\s\s+" , " ", body)
    whole_doc = title + body1
    doc = word_split(whole_doc)
    doc_cleaned = words_cleanup(doc)
    doc_cleaned_length = len(doc_cleaned)
    total_doc_length.append(doc_cleaned_length)
    
    
    
    #print(body1)
    #"doc" + str(i)
    
    #d['title'] = title
    d['doc' + str(i)] = body1
    d['doc' + str(i) + '_title'] = title
    #i+=1
    #print(d)
    doc = "doc" + str(i)
    #print(type(doc))
    #i+=1
    #print(doc)
    file_name = 'doc' + str(i) + '.txt'
    
    filepath = os.path.join('C:/Users/SVR/', file_name)
    #if not os.path.exists('C:\Users\SVR\'):
        #os.makedirs('c:/your/full/path')
    #f = open(filepath, "w")
    with open(filepath, "w") as f:
        f.write(whole_doc)
    i += 1
        
        #print("-----------------------------------------------------------------------------------------------------")
# List Of English Stop Words
# http://armandbrahaj.blog.al/2009/04/14/list-of-english-stop-words/

_STOP_WORDS = frozenset([
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 
        'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were', 'will', 'with'
])



def word_split(text):
    """
    Split a text in words. Returns a list of tuple that contains
    (word, location) location is the starting byte position of the word.
    """
    word_list = []
    wcurrent = []
    windex = None

    for i, c in enumerate(text):
        if c.isalnum():
            wcurrent.append(c)
            windex = i
        elif wcurrent:
            word = u''.join(wcurrent)
            word_list.append((windex - len(word) + 1, word))
            wcurrent = []

    if wcurrent:
        word = u''.join(wcurrent)
        word_list.append((windex - len(word) + 1, word))

    return word_list



def words_cleanup(words):
    """
    Remove words with length less then a minimum and stopwords.
    """
    cleaned_words = []
    for index, word in words:
        if word in _STOP_WORDS:
            continue
        cleaned_words.append((index, word))
    return cleaned_words

def words_normalize(words):
    """
    Do a normalization precess on words. In this case is just a tolower(),
    but you can add accents stripping, convert to singular and so on...
    """
    normalized_words = []
    for index, word in words:
        wnormalized = word.lower()
        normalized_words.append((index, wnormalized))
    return normalized_words

def word_index(text):
    """
    Just a helper method to process a text.
    It calls word split, normalize and cleanup.
    """
    words = word_split(text)
    words = words_normalize(words)
    words = words_cleanup(words)
    return words

def inverted_index(text):
    """
    Create an Inverted-Index of the specified text document.
        {word:[locations]}
    """
    inverted = {}

    for index, word in word_index(text):
        locations = inverted.setdefault(word, [])
        locations.append(index)

    return inverted

def inverted_index_add(inverted, doc_id, doc_index):
    """
    Add Invertd-Index doc_index of the document doc_id to the 
    Multi-Document Inverted-Index (inverted), 
    using doc_id as document identifier.
        {word:{doc_id:[locations]}}
    """
    for word, locations in doc_index.iteritems():
        indices = inverted.setdefault(word, {})
        indices[doc_id] = locations
    return inverted

def search(inverted, query):
    """
    Returns a set of documents id that contains all the words in your query.
    """
    words = [word for _, word in word_index(query) if word in inverted]
    results = [set(inverted[word].keys()) for word in words]
    return reduce(lambda x, y: x & y, results) if results else []

if __name__ == '__main__':

    # Build Inverted-Index for documents
    inverted = {}
    documents = d
    
    for doc_id, text in documents.iteritems():
        doc_index = inverted_index(text)
        inverted_index_add(inverted, doc_id, doc_index)

    # Print Inverted-Index
    for word, doc_locations in inverted.iteritems():
        print word, doc_locations

    # Search something and print results
    '''queries = ['Week', 'Niners week', 'West-coast Week', 'rated']
    for query in queries:
        result_docs = search(inverted, query)
        print "Search for '%s': %r" % (query, result_docs)
        for _, word in word_index(query):
            def extract_text(doc, index): 
                return documents[doc][index:index+20].replace('\n', ' ')

            for doc in result_docs:
                for index in inverted[word][doc]:
                    print '   - %s...' % extract_text(doc, index)
        print'''
