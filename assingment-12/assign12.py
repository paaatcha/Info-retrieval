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
from GA import GA


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
        
       
def fitness (data, params):
    # Verify if data is greater than zero
    v = data[:-1] < 0
    if v.sum() != 0:
        return 10
        
#    v = data[:-1] > 0
#    if v.sum() != 0:
#        return 10
    
    in_train = params[0] * data[:-1]
    out_train = params[1] 
    in_test = params[2] * data[:-1]
    out_test = params[3]
    k = params[4]
    
    res = knn (in_train, out_train, in_test, k)
#    print 1-((len(in_test) - contError (out_test, res))/45.0)
    return 1-((len(in_test) - contError (out_test, res))/45.0)
    

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
    
    IDF, acc = GA(4, 10, (0,4), fit_func=fitness, params=(in_train, out_train, in_test, out_test, k)) 
    
    print 'Iteration {}'.format(it)
    print 'IDF: {}'.format(IDF)
    print 'Accuracy: {}\n'.format(acc)
    
    
    res = knn (in_train * IDF[:-1], out_train, in_test * IDF[:-1], k)
    acc = ((len(in_test) - contError (out_test, res))/45.0)*100
    missKNN.append(acc)
    #print 'number of missclassification: ', acc



missKNN = np.asarray(missKNN)
print '*** Results KNN ***'
print 'AVG: ', missKNN.mean(), '\nSTD: ', missKNN.std()


