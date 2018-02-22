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

def isID (line, ID):    
    # checking the ID format        
    ID_str = '000'
    if ID >= 100:
        ID_str = '0'
    elif ID >= 10:
        ID_str = '00'                 
    
    r = False
    if line.replace('\n','') == (ID_str+str(ID)):
        r = True
        ID+=1
    elif line.replace('\n','') == (ID_str+str(ID+1)):
        r = True
        ID+=2
    elif line.replace('\n','') == (ID_str+str(ID+2)):
        r = True
        ID+=3
        
    return r, ID

def writeDoc (path, lines, ID):
    if not os.path.isdir(path+'/docs'):
        os.mkdir(path+'/docs')
        
    with open(path+'/docs/'+str(ID)+'.txt','w') as f:
        f.write(lines)

def processDocs (path, pathNew):
    with open(path,'r') as f:
        lines = f.readlines()
        
    ID = 1
    IDfil = 1
    k = 0    
    r = False
    # Removing some useless information
    lines = lines[27:-1]       
        
    while k < (len(lines)) and ID < 986:
        text = ''                
        while (r==False):
            if ID == 986:
                break
            text+=lines[k]
            k+=1
            r,ID = isID (lines[k], ID)           
            
        writeDoc(pathNew, text, IDfil)
        IDfil+=1
        r = False 
            
        
            
            
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
pathDoc = path + '/narrativas.txt'  
fold = '/docs'
foldaLine = 'docsaLine/'
pathFiles = path + fold

processDocs (pathDoc, path)

#filesList = generateFilesPath (pathFiles,True)
filesList = glob.glob(pathFiles+'/*')
s = len(filesList)
getNFilesPath (filesList,s)

k = int(sys.argv[1])
fil = 'filesPath.txt'

#aLineCmdIndex(fil, foldaLine)
#aLineCmdCluster (foldaLine, k, nIter=10)
#aLineCmdVecs (foldaLine)


dimVec = getDimVec (foldaLine+'dataset.conf')
#dimVec = getDimVec ('dataset.conf')
vecs = getVectors (foldaLine+'features.mtx', dimVec, s)
#vecs = getVectors ('features.mtx', dimVec, s)
dataClusters = clustersInDict (vecs, 'output.clustering')
centroids = getCentroids('centroids.mtx',k, dimVec) 


getMetricsTable (vecs, centroids, dataClusters, k)





