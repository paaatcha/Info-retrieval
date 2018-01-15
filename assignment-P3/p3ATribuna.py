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
from unidecode import unidecode
import io


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
        
def setSingleFile (filesList):
    text = ''
    i = 0
    for fil in filesList:
        print 'Writing the file: \n', fil
        # unicode(fil.replace(' ','').decode('utf-8'))
        text += '<DOC>\n\n<DOCNO>\nArquivo ' + str(i) + '\n</DOCNO>\n\n'
        i+=1
        # Getting the whole text from the txt
        with open(fil,'r') as f:
            text += f.read().decode('utf-8','ignore').encode("utf-8")
            #unidecode(f.read())
            text += '\n</DOC>\n\n'                      

    with open('aTribunaSingleFile.txt', 'w') as f:
        f.write(text)        


def getIndexingALine ():
    cmd = 'aLine -i -l filesPath.txt -d aLineTribuna'
    os.system(cmd)
    
def getIndexingZettair ():
    cmd = '/usr/local/zettair/bin/zet -i aTribunaSingleFile.txt'
    os.system(cmd)   

#################### STARTING THE SCRIPT ###########################

path = os.getcwd() # my actual path
pathFiles = path + '/aTribuna-21dir'  

checkingDataset (pathFiles)
filesList = generateFilesPath (pathFiles,True)
setSingleFile (filesList)


##############################  aLINE and Zettair  ####################################
getIndexingALine()

getIndexingZettair()








