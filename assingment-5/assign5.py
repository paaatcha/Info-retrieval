#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Author: André Pacheco
Email: pacheco.comp@gmail.com

This file contains the solution fot assignment 4
"""

import os
import glob
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# checking if the files was downloaded
path = os.getcwd() # my actual path
isDown = os.path.isdir(path+'/aTribuna-21dir')
pathFiles = path + '/aTribuna-21dir'

# Downloading the directory if it does not exist
if (not isDown): 
    print 'Downloading the Tribuna database...'
    os.system('wget http://www.inf.ufes.br/~elias/dataSets/aTribuna-21dir.tar.gz')    
    os.system('mkdir aTribuna-21dir')
    print 'Extracting the Tribuna database...'
    os.system('tar -xzf aTribuna-21dir.tar.gz -C '+ pathFiles)        
    os.system('rm -rf aTribuna-21dir.tar.gz')
    print 'The files have been set'
else:
    print 'The database has already downloaded'    
    
# Removing the classes.txt and Desc-classes.txt from the root folder
if os.path.isfile(pathFiles+'/classes.txt'):
    os.system('rm ' + pathFiles+'/classes.txt')
if os.path.isfile(pathFiles+ '/Desc-classes.txt'):
    os.system('rm ' + pathFiles+ '/Desc-classes.txt')

allFolders = glob.glob(pathFiles+'/*')
#print len(allFolders)

# This var will be the dictionary containing all the words
totalWords = Counter()

# Counting the number of files
nFiles = 0
print 'Computing the 10 most frequent words...'

for folder in allFolders:
    print 'Loading files in ' + folder
    allFiles = glob.glob(folder+'/*.txt')
    
    for fil in allFiles:
        arch = open (fil,'r')
        nFiles += 1
        
        for word in arch.read().replace(',','').replace('.','').replace(':','').replace(';','').replace('!','').replace('?','').lower().split():
            totalWords[word] += 1
                
        arch.close()
                   
# Getting the most 10 common words
most10 = totalWords.most_common(10)        
word1 = most10[0][0]
word2 = most10[1][0]

print '\nThe most 2 frequent words are: [' + word1 + '] and [' + word2 + ']\n'

# This var will store all frequencies of word1 and word2 for each documento
freqWordsDoc = np.zeros([nFiles,2])
filePos = 0

print 'Computing the frequency of these word for all documents...\n'
for folder in allFolders:
    print 'Loading files in ' + folder
    allFiles = glob.glob(folder+'/*.txt')
    
    for fil in allFiles:
        arch = open (fil,'r')        
        
        for word in arch.read().replace(',','').replace('.','').replace(':','').replace(';','').replace('!','').replace('?','').lower().split():
            if word == word1:
                freqWordsDoc[filePos,0] += 1
            elif word == word2:
                freqWordsDoc[filePos,1] += 1
    
        filePos += 1
                
        arch.close()

# Plotting the 2D graph
plt.axis([0,450,0,140])
sc = plt.scatter(freqWordsDoc[:,0], freqWordsDoc[:,1])
plt.xlabel('Word = '+ word1)
plt.ylabel('Word = '+ word2)
plt.title('All documents represented by a 2D graph')
plt.show()







