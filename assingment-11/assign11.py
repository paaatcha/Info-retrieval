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
    arch = open ('filesPath'+str(size)+'.txt', 'w')
    
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
        
def aLineCmdIndex (fil, fold):    
    cmd = 'aLine -i -l ' + fil + ' -d '+ fold
    os.system(cmd)    
    
def aLineCmdCluster (fold, k=3, nIter=200):    
    cmd = 'aLine --clustering --algorithm kmeans --features '+ fold +'/cache.txt -k '+ str(k) +' --num-inter '+ str(nIter)
    os.system(cmd)

def aLineCmdVecs (fold):
    cmd = 'aLine -d '+ fold +' --convert'
    os.system(cmd)

def getDimVec (path):    
    with open(path,'r') as f:        
        dim = int(f.readlines()[1].split(':')[1])        
    return dim
    
def getVectors (path, dim, s):
    feat = np.loadtxt(path,skiprows=2,dtype=np.int32)
    vecs = np.zeros((s,dim))    
    
    for f in feat:
        vecs[f[0]-1, f[1]-1] = f[2]        
    
    return vecs
    

def cosSimilarity (x,y):
    out = (x.dot(y))/(np.linalg.norm(x)*np.linalg.norm(y))
    if math.isnan(out):
        out = 0
    return out

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
#        print centroid
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



def getCentroids (path, k, dim):
    feat = np.loadtxt(path,skiprows=2)    
    #dim = int(feat[0,2])
    cents = np.zeros((k,dim))        
        
    for f in feat:
        cents[int(f[0]-1), int(f[1]-1)] = f[2]        
    
    return cents

def clustersInDict(irisIn, pathOut):
    outClusters = np.loadtxt(pathOut)
    
    irisClusters = dict()

    for i in range(int(outClusters.max())+1):
        irisClusters[i] = list()
    
    for i in xrange(len(outClusters)):
        irisClusters[outClusters[i]].append(irisIn[i])
        
    return irisClusters

def getMetricsTable (data, cents, dataClusters, K):
    #checkAccuracy ('iris_class.txt', 'output.clustering')
    den, avgDen = getDensity(data)
    print 'Data set density: {}\nAverage of the density: {} \n'.format(den, avgDen)
    
   
    gCluster = cents.mean(axis=0)
    
    den = 0
    for i in range(K):
        den += getDensityToCluster (dataClusters[i], cents[i])
        
    print 'AVG similarity between docs and corresponding centroids (x): ', den/K, '\n'
    x = den/K
    
    den = getDensityToCluster (cents, gCluster)
    print 'AVG similarity between centroids and main centroid: ', den, '\n'
    
    _,den = getDensity (cents)
    print 'AVG similarity between pairs of cluster centroids (y): ', den, '\n'
    y = den
    
    print 'Ratio y/x: ', y/x    


#################### STARTING THE SCRIPT ###########################

path = os.getcwd() # my actual path
pathFiles = path + '/aTribuna-21dir'  
fold = 'aTribuna'

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

dimVec = getDimVec (fold+'/dataset.conf')
#dimVec = getDimVec ('dataset.conf')
vecs = getVectors (fold+'/features.mtx', dimVec, s)
#vecs = getVectors ('features.mtx', dimVec, s)
dataClusters = clustersInDict (vecs, 'output.clustering')
centroids = getCentroids('centroids.mtx',k, dimVec) 


getMetricsTable (vecs, centroids, dataClusters, k)





