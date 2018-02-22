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
            f.write(sample)    
            f.write('\n')  


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
                f.write(irisOut[i]+'\n')
    
def checkAccuracy (real, predict):
    with open(real,'r') as f:
        real = f.readlines()
        
    with open(predict,'r') as f:
        predict = f.readlines()
 
    print real
    print predict
    
    
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

    
def aLineCmd (k=3):
    cmd = 'aLine --classifier --algorithm knn --features iris_data.mtx --train iris_train.txt --test iris_test.txt --labels iris_class.txt -k '+str(k)+' -o iris_class_predict.txt'
    os.system(cmd)



path = os.getcwd() # my actual path
pathIris = path + '/iris'  

checkingDataset(pathIris)
irisIn, irisOut = getIris(pathIris)

generateIdsTrainTest (len(irisIn), irisOut=irisOut)
aLineCmd(7)
checkAccuracy ('iris_class_test.txt', 'iris_class_predict.txt')
den, avgDen = getDensity(irisIn)
print 'Data set density: {}\nAverage of the density: {}'.format(den, avgDen)







