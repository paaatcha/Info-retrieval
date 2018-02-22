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
os.system('rm ' + pathFiles+'/classes.txt ' + pathFiles+ '/Desc-classes.txt')



allFolders = glob.glob(pathFiles+'/*')
#print len(allFolders)

# This var will be the dictionary containing all the words
totalWords = Counter()

for folder in allFolders:
    print 'Loading files in ' + folder
    allFiles = glob.glob(folder+'/*.txt')
    
    for fil in allFiles:
        arch = open (fil,'r')
        
        for word in arch.read().replace(',','').replace('.','').replace(':','').replace(';','').replace('!','').replace('?','').lower().split():
            totalWords[word] += 1
                
        arch.close()
                   
# Print the most 10 common words
most10 = totalWords.most_common(10)        
print most10

# Writing to a file the most 10 common words
outFile = open ('arquivosaida.txt', 'w')
outFile.write ('Word -- Frequency\n')
outFile.write ('\n'.join('%s %s' % x for x in most10))
outFile.close()


