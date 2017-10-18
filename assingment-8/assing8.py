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
        
# Euclidean distance
def distance (x,y):
    x = np.asarray(x)
    y = np.asarray(y)
    return np.sqrt(np.power(x-y,2).sum(axis=0))        
        
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
            
    with open('iris_class.txt','w') as f:
        f.write('\n'.join(irisOut))           

    return irisIn, irisOut

def generateMtx (irisIn):
    m,n = irisIn.shape
    arch = open('iris.mtx','w')
    arch.write (str(m)+' '+str(m)+' '+str(m*m)+'\n')
    mtx = list()
    for i1 in xrange(m):
        for i2 in xrange(m):
            #arch.write(str(i1+1)+' '+str(i2+1)+' '+str(distance(irisIn[i1,:], irisIn[i2,:]))+'\n')
            mtx.append([i1+1, i2+1, distance(irisIn[i1,:], irisIn[i2,:])])
            
    # Normalizing
    mtx = np.asarray(mtx)
    mtxMax = mtx[:,2].max()    
    mtx[:,2] = 1-(mtx[:,2]/mtxMax)
    
    for m in mtx:
        arch.write(str(int(m[0]))+' '+str(int(m[1]))+' '+str(m[2])+'\n')
    
    arch.close()
    
    

def generateIdsTrainTest (siz, perc='0.3'):
    nTest = int(round(150*perc))
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
    
def checkAccuracy (real, predict):
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
    print (acc/nReal)*100


path = os.getcwd() # my actual path
pathIris = path + '/iris'  

checkingDataset(pathIris)
irisIn, irisOut = getIris(pathIris)
generateMtx(irisIn)

generateIdsTrainTest (len(irisIn))
