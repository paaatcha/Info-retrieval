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
from itertools import combinations

sys.path.append ('Google')
from google2 import search


def formatText (text):
    text = text.replace(',','').replace('.','').replace(':','').replace(';','')
    text = text.replace('!','').replace('?','').replace('\'','').replace('\"','')
    
    return text

def loadQuery (path):
    allQueries = list()
    with open(path,'r') as f:
        lines = f.readlines()
    for q in lines:    
        if len(q) > 5:
            allQueries.append(removeStopWords(q).split())
        
    return allQueries
        
    
    
    return q

def removeStopWords (text):
    text = formatText (text)
    with open('stop-words','r') as f:
        stopWords = f.read().replace(' ','').decode('utf-8').split('\n')
        
    text = text.lower().split()
    newText = list()
    for word in text:        
        if word not in stopWords:
            newText.append(word)    

    result = ' '.join(newText)
    return result

def isHTML (url):
    typ = url.split('/')[-1].split('.')[-1].lower()
    if typ == 'pdf' or typ == 'doc' or typ == 'docx':
        return False
    else:
        return True

def getURLsFromQuery (query):
    sg = search(query, tld='com', lang='pt-br', num=5, stop=2, only_standard=True)
    #sg = ['http://www.pachecoandre.com.br']
    
    allTexts = list()   
    allURLs = list()
    for url in sg:    
        print 'URLs encontrada: \n', url, '\n'
        if isHTML (url):
            allURLs.append(url)
            html = urllib.urlopen(url).read()
            soup = BeautifulSoup(html, "html")
        
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

def compare (wordsQuery, fullText, URL, sizeCompT=100, sizeCompQ=100, threshold=0.3):
    wordsText = removeStopWords(fullText).split(' ')
    sizeText = len(wordsText)     

    sizeQuery = len(wordsQuery)

    if sizeCompT > sizeText:
        sizeCompT = sizeText
    if sizeCompQ > sizeQuery:
        sizeCompQ = sizeQuery
    
    output = ''
    for offset_q in range(0,sizeQuery,sizeCompQ):
        end_q = offset_q + sizeCompQ
        compQuery = ' '.join(wordsQuery[offset_q:end_q])         

        for offset in range(0,sizeText,sizeCompT):
            end = offset + sizeCompT
            compText = ' '.join(wordsText[offset:end])    
            ratio = SequenceMatcher(None,compQuery,compText).ratio()
            
            
            
            if ratio > threshold:                
                output += '<cpy metric=cos sim={} href={}>\n'.format(ratio,URL)
                output += compQuery
                output += '\n</cpy>\n\n'               
                
    return output
                
            

        
        

#################### STARTING THE SCRIPT ###########################
pathQuery = 'query.txt'
fullQuery= loadQuery (pathQuery)

output = ''
b=1
nw = 15
for query in fullQuery: 
    if nw > len(query):
        nw = len(query)
    smallQuery = ' '.join(query[0:nw])
    print 'Busca {}...\n'.format(b)
    allTexts, allURLs = getURLsFromQuery(smallQuery)
    b+=1
    
    for k in range(len(allTexts)):
        output += compare (query, allTexts[k], allURLs[k])
    
with open('Resultado.txt', 'w') as f:
    f.write(output)
    








