#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Author: André Pacheco
Email: pacheco.comp@gmail.com


"""

import os
import sys
import glob
from collections import Counter
import numpy as np
from random import shuffle
from time import time
import subprocess


def generateFilesPath (path,shuf=False):
    allFolders = glob.glob(path+'/*')
    allFiles = list()
    for folder in allFolders:
        #print 'Loading files in ' + folder
        allFiles += glob.glob(folder+'/*.docx')
        
    if shuf:
        shuffle(allFiles)
        
    return allFiles

def checkingDataset (path):     
    # checking if the files was downloaded    
    isDown = os.path.isdir(path)
       
    # Downloading the directory if it does not exist
    if (not isDown): 
        print 'Downloading the usielCarneiro database...'
        os.system('wget http://www.inf.ufes.br/~elias/dataSets/usielCarneiro.tar.gz')    
        os.system('mkdir usielCarneiro')
        print 'Extracting the usielCarneiro database...'
        os.system('tar -xzf usielCarneiro.tar.gz -C '+ pathFiles)        
        os.system('rm -rf usielCarneiro.tar.gz')
        print 'The files have been set'
    else:
        print 'The database has been already downloaded'


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
    print 'Indexing the database using E12...'
    
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
pathFiles = path + '/usielCarneiro'  

checkingDataset (pathFiles)
filesList = generateFilesPath (pathFiles)
print len(filesList)

#sizes = [1000, 2000, 4000, 16000, 32000, len(filesList)]

# The number of files to be indexing is get through the command line
# For example: python assing6.py 1000
#s = [int(sys.argv[1])]
#nIterations = 15
#
#fil = 'filesPath' + str(s[0]) + '.txt'
#timeE12 = []
#timeALine = []
#out = 'Results for '+ str(s[0]) + ' files\n'
#
#for i in xrange(nIterations):
#    getNFilesPath (filesList,s)
#    out = out + '******** ITERATION ' + str(i+1) + '********\n\n'
#    # performing the E12 algorithm
#    wordsE12, tE12 = indexing (fil)
#    timeE12.append(tE12)
#    out = out + '*** E12 ***\n' + str(timeE12) + '\n'
#    
#    # Performing the aLine. Creating the cmd line
#    cmd = 'aLine -i -l ' + fil + ' -d aLine' + str(s[0])
#    taux = time()
#    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
#    timeALine.append(time()-taux)
#    (outaLine, err) = proc.communicate()
#    out = out + '*** aLine ***\n' + outaLine + '\n'
#
#    print 'Iteration: ', i
#
#
#timeE12 = np.asarray(timeE12)
#timeALine = np.asarray(timeALine)
#print '\n*** Statistics ***'
#print 'E12 mean: ', timeE12.mean(),' - E12 std: ', timeE12.std()
#print 'aLine mean: ', timeALine.mean(),' - aLine std: ', timeALine.std(), '\n'
#
## Writing a file with the outputs
#arch = open('resultsLog'+str(s[0])+'.txt','w')
#arch.write(out)
#arch.close()






