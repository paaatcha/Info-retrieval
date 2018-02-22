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
import glob
from collections import Counter
import numpy as np
from random import shuffle
from time import time
import subprocess
import math
from metrics import *


def generateFilesPath (path,shuf=False):
    allFolders = glob.glob(path+'/*')
    allFiles = list()
    for folder in allFolders:
        #print 'Loading files in ' + folder
        allFiles += glob.glob(folder+'/*.txt')
        
    if shuf:
        shuffle(allFiles)
        
    return allFiles

def getNFilesPath (filesList, size):     
    print 'Writing the output with ' + str(size) + ' files'
    arch = open ('filesPath.txt', 'w')
    
    for i in xrange(size):       
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
        


#################### STARTING THE SCRIPT ###########################

path = os.getcwd() # my actual path
pathFiles = path + '/aTribuna-21dir'  
fold = 'aTribuna/'

checkingDataset (pathFiles)
filesList = generateFilesPath (pathFiles,True)

s = int(sys.argv[1])
k = int(sys.argv[2])
fold = fold
getNFilesPath (filesList,s)
fil = 'filesPath.txt'

aLineCmdIndex(fil, fold)
aLineCmdCluster (fold, k, nIter=10)
aLineCmdVecs (fold)

dimVec = getDimVec (fold+'dataset.conf')
#dimVec = getDimVec ('dataset.conf')
vecs = getVectors (fold+'features.mtx', dimVec, s)
#vecs = getVectors ('features.mtx', dimVec, s)
dataClusters = clustersInDict (vecs, 'output.clustering')
centroids = getCentroids('centroids.mtx',k, dimVec) 


getMetricsTable (vecs, centroids, dataClusters, k)





