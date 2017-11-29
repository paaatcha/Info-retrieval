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

def cosSimilarity (x,y):
    x = np.asarray(x)
    y = np.asarray(y)
    return (x.dot(y))/(np.linalg.norm(x)*np.linalg.norm(y))

def getDensity (irisIn):
    m,n = irisIn.shape
    den = 0
    for i1 in xrange(m):
        for i2 in xrange(m):            
            den += cosSimilarity(irisIn[i1,:], irisIn[i2,:])
    
    # Taking off the values when i=j
    den -= m        
    denMean = den/(m*m)
    
    return den, denMean
    
def getDensityToCluster (data, centroid):
    data = np.asarray(data)       
    m,n = data.shape
    den = 0
    for i in xrange(m):
        den += cosSimilarity(data[i], centroid)        
        
    return den/m

def checkAccuracy (real, predict):
    with open(real,'r') as f:
        real = f.readlines()
        
    with open(predict,'r') as f:
        predict = f.readlines()
 
    #print real
    #print predict
    
    
    nReal = len(real)
    nPredict = len(predict)
    
    if nReal != nPredict:
        print 'The number of nReal is different than nPredict\n'
        raise ValueError
    
    acc = 0
    for vr,vp in zip(real,predict):
        if vr == vp:
            acc += 1
    
    # Priting the final accuracy
    print 'Correct predictions: ', acc, ' of ', nReal
    return acc

    
def aLineCmdCluster (k=3, nIter=200):    
    cmd = 'aLine --clustering --algorithm kmeans --features aLine100/cache.txt -k '+ str(k) +' --num-inter '+ str(nIter)
    os.system(cmd)

def getCentroids (centroids):
    cent = np.loadtxt('centroids.mtx', skiprows=1)
    nCent = int(cent[0,2]/4)
    cents = list()
    
    for i in range(1,nCent*4,4):
        cents.append(cent[i:i+4,2])
    
    return np.asarray(cents)

def clustersInDict(irisIn, pathOut):
    outClusters = np.loadtxt(pathOut)
    
    irisClusters = dict()

    for i in range(int(outClusters.max())+1):
        irisClusters[i] = list()
    
    for i in xrange(len(outClusters)):
        irisClusters[outClusters[i]].append(irisIn[i])
        
    return irisClusters


def aLineCmdIndex (fil, s):    
    cmd = 'aLine -i -l ' + fil + ' -d aLine' + str(s[0])
    os.system(cmd)


#################### STARTING THE SCRIPT ###########################

path = os.getcwd() # my actual path
pathFiles = path + '/aTribuna-21dir'  

checkingDataset (pathFiles)
filesList = generateFilesPath (pathFiles,True)



# The number of files to be indexing is get through the command line
# For example: python assing6.py 1000
s = [int(sys.argv[1])]
getNFilesPath (filesList,s)
fil = 'filesPath' + str(s[0]) + '.txt'

aLineCmdIndex (fil, s)







