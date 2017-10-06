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
from random import shuffle
from time import time


def generateFilesPath (path,shuf=False):
    allFolders = glob.glob(path+'/*')
    allFiles = list()
    for folder in allFolders:
        #print 'Loading files in ' + folder
        allFiles += glob.glob(folder+'/*.txt')
        
    if shuf:
        shuffle(allFiles)
        
    return allFiles

def getNFilesPath (filesList, sizes):    
    for k in xrange(len(sizes)):        
        print 'Writing the output with ' + str(sizes[k]) + ' files'
        arch = open ('filesPath'+str(sizes[k])+'.txt', 'w')
        
        for i in xrange(sizes[k]):       
            arch.write(filesList[i]+'\n')
            
        arch.close()
    
    
def checkingDataset (path):     
    # checking if the files was downloaded    
    isDown = os.path.isdir(path)
       
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

def indexing (path):
    initTime = time()
    arch = open(path,'r')
    allPaths = arch.readlines()
    arch.close()    
       
    # This var will be the dictionary containing all the words
    totalWords = Counter()
    
    # Just to follow the process
    N = len(allPaths)
    k = 1
    print 'Computing the 10 most frequent words...'
    
    for pa in allPaths:        
        arch = open (pa[:-1],'r')
        #print 'Loading file ', k, ' of ', N
        for word in arch.read().replace(',','').replace('.','').replace(':','').replace(';','').replace('!','').replace('?','').lower().split():
            totalWords[word] += 1
        
        arch.close()
        k+=1
    
    endTime = time()
        
    #print totalWords.most_common(10)
    return totalWords, (endTime-initTime)


#################### STARTING THE SCRIPT ###########################

path = os.getcwd() # my actual path
pathFiles = path + '/aTribuna-21dir'  

checkingDataset (pathFiles)
filesList = generateFilesPath (pathFiles,True)

#sizes = [1000, 2000, 4000, 16000, 32000, len(filesList)]
sizes = [1000]

getNFilesPath (filesList, sizes)

time45 = []
for i in xrange(15):
    words45, t = indexing ('filesPath1000.txt')
    time45.append(t)

print words45.most_common(10)
time45 = np.asarray(time45)
print time45.mean(), time45.std()







