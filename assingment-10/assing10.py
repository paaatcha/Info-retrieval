#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Author: André Pacheco
Email: pacheco.comp@gmail.com


"""


import os
import numpy as np
from random import shuffle

def checkingDataset (path):     
    # checking if the files was downloaded    
    isDown = os.path.isdir(path)
       
    # Downloading the directory if it does not exist
    if (not isDown): 
        print 'Downloading the iris database...'
        os.system('wget https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data')    
        os.system('mkdir iris')
        os.system('mv iris.data iris')
        print 'The file has been set'
    else:
        print 'The database has already been downloaded'
        
       
def getIris (path):
    irisIn = np.loadtxt(path+'/iris.data',delimiter=',',usecols=(0,1,2,3))
    irisOut = list()
    with open(path+'/iris.data') as f:
        lines = f.read().splitlines()
        for l in lines:            
            try:
                irisOut.append(l.split(',')[4])
            except IndexError:
                pass
            
   
    with open('iris_data.mtx','w') as f:
        f.write('% Matrix Market\n')
        f.write(str(irisIn.shape[0])+' '+str(irisIn.shape[1])+' '+str(irisIn.shape[0]*irisIn.shape[1])+'\n')
        for i1 in range(irisIn.shape[0]):
            for i2 in range(irisIn.shape[1]):
                f.write(str(i1+1)+' '+str(i2+1)+' '+str(irisIn[i1,i2])+'\n')
    
    with open('iris_class.txt','w') as f:
        for sample in irisOut: 
            if sample == 'Iris-setosa':
                out = 0
            elif sample == 'Iris-versicolor':
                out = 1
            elif sample == 'Iris-virginica':
                out = 2                    
            f.write(str(out)+'\n')

    return irisIn, irisOut

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


def generateIdsTrainTest (siz, perc='0.3',irisOut=None):
    nTest = int(round(150*0.3))
    allIds = range(siz)
    shuffle(allIds)
    
    print 'Number of train\'s sample: ', len(allIds[:nTest])
    print 'Number of test\'s sample: ',len(allIds[nTest:])
    
    with open('iris_test.txt','w') as f:
        for i in allIds[:nTest]:
            f.write(str(i)+'\n')
            
    with open('iris_train.txt','w') as f:
        for i in allIds[nTest:]:
            f.write(str(i)+'\n')        
            
    if irisOut is not None:
        with open('iris_class_test.txt','w') as f:
            for i in allIds[:nTest]:
                if irisOut[i] == 'Iris-setosa':
                    out = 0
                elif irisOut[i] == 'Iris-versicolor':
                    out = 1
                elif irisOut[i] == 'Iris-virginica':
                    out = 2                    
                f.write(str(out)+'\n')
    
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

    
def aLineCmd (k=3, nIter=200):    
    cmd = 'aLine --clustering --algorithm kmeans --features iris_data.mtx -k '+ str(k) +' --num-inter '+ str(nIter)
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


path = os.getcwd() # my actual path
pathIris = path + '/iris'  
K = 3

checkingDataset(pathIris)
irisIn, irisOut = getIris(pathIris)

#aLineCmd()
checkAccuracy ('iris_class.txt', 'output.clustering')
den, avgDen = getDensity(irisIn)
print 'Data set density: {}\nAverage of the density: {} \n'.format(den, avgDen)

irisClusters = clustersInDict (irisIn, 'output.clustering')
cents = getCentroids ('centroids.mtx')
gCluster = cents.mean(axis=0)

den = 0
for i in range(K):
    den += getDensityToCluster (irisClusters[i], cents[i])
    
print 'AVG similarity between docs and corresponding centroids (x): ', den/K, '\n'
x = den/K

den = getDensityToCluster (cents, gCluster)
print 'AVG similarity between centroids and main centroid: ', den, '\n'

_,den = getDensity (cents)
print 'AVG similarity between pairs of cluster centroids (y): ', den, '\n'
y = den

print 'Ratio y/x: ', y/x





