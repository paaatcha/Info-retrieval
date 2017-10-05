#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Author: André Pacheco
Email: pacheco.comp@gmail.com

This file contains the solution fot assignment 1
"""

import os
import glob
import numpy as np

# checking if the files was downloaded
path = os.getcwd() # my actual path
isDown = os.path.isdir(path+'/estatistica-metricas')


# Downloading the directory if it does not exist
if (not isDown): 
    os.system('mkdir estatistica-metricas')       
    os.system('wget http://www.inf.ufes.br/~elias/dataSets/estatistica-metricas.rar')        
    os.system('unrar x estatistica-metricas.rar')    
    os.system('rm -rf estatistica-metricas.rar')
    os.system ('mv *.dat estatistica-metricas')
    
allFiles = glob.glob(path+'/estatistica-metricas/*.dat')
datasList = list()

# Getting the values from the files
for fil in allFiles:
    datasList.append (np.genfromtxt(fil))   
    
dataMatrix = (np.asarray(datasList)).T

print 'A matrix with shape =', dataMatrix.shape, 'was loaded'




