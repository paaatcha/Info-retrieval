#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Author: André Pacheco
Email: pacheco.comp@gmail.com


"""
import os
import glob
from collections import Counter
import numpy as np
from random import shuffle
from docx import Document
from nltk import ngrams
import json

def generateFilesPath (path,shuf=False,fileFormat='txt'):
    allFolders = glob.glob(path+'/*')
    allFiles = list()
    for folder in allFolders:
        #print 'Loading files in ' + folder
        allFiles += glob.glob(folder+'/*.'+fileFormat)
        
    if shuf:
        shuffle(allFiles)
        
    return allFiles

def writeNFilesPath (filesList, size, name=None):    
    if name is None:
        print 'Writing the output with ' + str(size) + ' files'
        path = 'filesPath'+str(size)+'.txt'
        arch = open (path, 'w')
    else:
        print 'Writing the output for ' + name + ' files'
        path = 'filesPath'+name+'.txt'
        arch = open (path, 'w')        
    
    for i in xrange(size):       
        arch.write(filesList[i]+'\n')
        
    arch.close()
    return path


def checkingDataset (path):     
    # checking if the files was downloaded    
    isDown = os.path.isdir(path)
       
    # Downloading the directory if it does not exist
    if (not isDown): 
        print 'Downloading the usielCarneiro database...'
        os.system('wget http://www.inf.ufes.br/~elias/dataSets/usielCarneiro.tar.gz')    
        os.system('mkdir usielCarneiro')
        print 'Extracting the usielCarneiro database...'
        os.system('tar -xzf usielCarneiro.tar.gz -C '+ pathFiles)        
        os.system('rm -rf usielCarneiro.tar.gz')
        print 'The files have been set'
    else:
        print 'The database has already been downloaded'

def docx2txt (filesList):
    for fil in filesList:
        # updating the files name to .txt        
        nameTxt = fil[0:-4]+'txt'
        isDown = os.path.isfile(nameTxt)
        if (not isDown):
            print 'Writing the file: \n', nameTxt
            
            # Getting the whole text from the docx
            doc = Document(fil)
            fullText = ''
            for p in doc.paragraphs:
                fullText += p.text + '\n'

            # Writing the .txt file
            arch = open (nameTxt, 'w')
            arch.write(fullText)
            arch.close()


def getIndexingALine ():
    cmd = 'aLine -i -l filesPathUsiel.txt -d aLineUsiel'
    os.system(cmd)

#################### STARTING THE SCRIPT ###########################

path = os.getcwd() # my actual path
pathFiles = path + '/usielCarneiro'  

# Cheking the database and download it if needs
checkingDataset (pathFiles)

# Getting the docx paths
filesListDocx = generateFilesPath (pathFiles, fileFormat='docx')

# Converting the docx to txt
docx2txt(filesListDocx)

# Getting the txt paths
filesListTxt = generateFilesPath (pathFiles, fileFormat='txt')
n = len(filesListTxt)

# Writting the file of paths
pathFiles = writeNFilesPath (filesListTxt,n,'Usiel')


##############################  aLINE  ####################################
getIndexingALine()

# http://www.daviddlewis.com/resources/testcollections/reuters21578/reuters21578.tar.gz
# http://ir.dcs.gla.ac.uk/resources/test_collections/



