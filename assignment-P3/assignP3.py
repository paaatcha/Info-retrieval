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

#################### STARTING THE SCRIPT ###########################

path = os.getcwd() # my actual path
pathFiles = path + '/aTribuna-21dir'  

checkingDataset (pathFiles)
filesList = generateFilesPath (pathFiles,True)

#sizes = [1000, 2000, 4000, 16000, 32000, len(filesList)]

# The number of files to be indexing is get through the command line
# For example: python assing6.py 1000
s = [int(sys.argv[1])]
nIterations = 15

fil = 'filesPath' + str(s[0]) + '.txt'
timeALine = []
out = 'Results for '+ str(s[0]) + ' files\n'

for i in xrange(nIterations):
    getNFilesPath (filesList,s)    
    
    # Performing the aLine. Creating the cmd line
    cmd = 'aLine -i -l ' + fil + ' -d aLine' + str(s[0])
    taux = time()
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    timeALine.append(time()-taux)
    (outaLine, err) = proc.communicate()
    out = out + '*** aLine ***\n' + outaLine + '\n'

    print 'Iteration: ', i


timeALine = np.asarray(timeALine)
print '\n*** Statistics ***'
print 'aLine mean: ', timeALine.mean(),' - aLine std: ', timeALine.std(), '\n'

# Writing a file with the outputs
arch = open('resultsLog'+str(s[0])+'.txt','w')
arch.write(out)
arch.close()






