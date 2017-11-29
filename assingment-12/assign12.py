#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Author: André Pacheco
Email: pacheco.comp@gmail.com


"""

import os
import numpy as np
from random import shuffle
from knn import knn
from utilsClassification import ind2vec, contError


def checkingDataset (path):     
    # checking if the files was downloaded    
    isDown = os.path.isdir(path)
    print path
       
    # Downloading the directory if it does not exist
    if (not isDown): 
        print 'Downloading the iris database...'
        os.system('wget https://raw.githubusercontent.com/paaatcha/machine-learning/master/datasets/iris.csv')    
        os.system('mkdir iris')
        os.system('mv iris.csv iris')
        print 'The file has been set'
    else:
        print 'The database has already been downloaded'
        
       

path = os.getcwd() # my actual path
pathIris = path + '/iris'  
checkingDataset(pathIris)

dataset = np.genfromtxt('iris/iris.csv', delimiter=',')

############################### KNN ###########################################
# Number of samples and features + label (the last position of the array is the class label)
[nsp, feat] = dataset.shape
nIter = 30
missKNN = list()
k = 11

for it in range(nIter):    
    # Shuffling the dataset
    np.random.shuffle(dataset)

############################## KNN ###########################################    
    # Getting 70% for training and 30% for tests
    sli = int(round(nsp*0.7))
    in_train = dataset[0:sli,0:feat-1]
    out_train = ind2vec((dataset[0:sli,feat-1])-1)
    in_test = dataset[sli:nsp,0:feat-1]
    out_test = ind2vec(dataset[sli:nsp,feat-1]-1)
    
    res = knn (in_train, out_train, in_test, k)
    acc = ((len(in_test) - contError (out_test, res))/45.0)*100
    missKNN.append(acc)
    #print 'number of missclassification: ', acc



missKNN = np.asarray(missKNN)
print '*** Results KNN ***'
print 'AVG: ', missKNN.mean(), '\nSTD: ', missKNN.std()


