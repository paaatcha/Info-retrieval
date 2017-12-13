#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Author: André Pacheco
Email: pacheco.comp@gmail.com

Example of use:
python assing6.py N
N is the number of files to be indexed.

"""

import os
import sys
import numpy as np
from time import time
import subprocess
import urllib
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

sys.path.append ('Google')
from google2 import search


def formatText (text):
    text = text.replace(',','').replace('.','').replace(':','').replace(';','')
    text = text.replace('!','').replace('?','').replace('\'','').replace('\"','')
    
    return text

def loadQuery (path):
    with open(path,'r') as f:
        q = formatText(f.read())
    q = removeStopWords(q)        
    q = q.split()
    print len(q)
    
    return q

def removeStopWords (text):
    with open('stop-words','r') as f:
        stopWords = f.read().replace(' ','').decode('utf-8').split('\n')
        
    text = text.lower().split()
    newText = list()
    for word in text:        
        if word not in stopWords:
            newText.append(word)    

    result = ' '.join(newText)
    return result


def getURLsFromQuery (query):
    sg = search(query, tld='com', lang='pt-br', stop=5)
    #sg = ['http://www.pachecoandre.com.br']
    
    allTexts = list()   
    allURLs = list()
    for url in sg:    
        print url, '\n'
        allURLs.append(url)
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html)
    
        # killing all script and style elements
        for script in soup(["script", "style"]):
            script.extract()
    
        # getting the text
        text = soup.get_text()  
        
        # Formating the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        allTexts.append(text)
        text = ''

    return allTexts, allURLs

 


#################### STARTING THE SCRIPT ###########################
pathQuery = 'query.txt'
query = loadQuery (pathQuery)

print query
#allTexts, allURLs = getURLsFromQuery(query)
    

#similarity_ratio = SequenceMatcher(None,removeStopWords(comp), removeStopWords(text)).ratio()
#print similarity_ratio  #plagiarism detected   




#removeStopWords (text)







