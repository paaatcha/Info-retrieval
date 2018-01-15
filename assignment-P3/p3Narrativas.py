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

def isID (line, ID):    
    # checking the ID format        
    ID_str = '000'
    if ID >= 100:
        ID_str = '0'
    elif ID >= 10:
        ID_str = '00'                 
    
    r = False
    if line.replace('\n','') == (ID_str+str(ID)):
        r = True
        ID+=1
    elif line.replace('\n','') == (ID_str+str(ID+1)):
        r = True
        ID+=2
    elif line.replace('\n','') == (ID_str+str(ID+2)):
        r = True
        ID+=3
        
    return r, ID

def writeDoc (path, lines, ID):
    if not os.path.isdir(path+'/docs'):
        os.mkdir(path+'/docs')
        
    with open(path+'/docs/'+str(ID)+'.txt','w') as f:
        f.write(lines)

def processDocs (path, pathNew):
    with open(path,'r') as f:
        lines = f.readlines()
        
    ID = 1
    IDfil = 1
    k = 0    
    r = False
    # Removing some useless information
    lines = lines[27:-1]       
        
    while k < (len(lines)) and ID < 986:
        text = ''                
        while (r==False):
            if ID == 986:
                break
            text+=lines[k]
            k+=1
            r,ID = isID (lines[k], ID)           
            
        writeDoc(pathNew, text, IDfil)
        IDfil+=1
        r = False 
            
        
            
            
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
    arch = open ('filesPathNarrativas.txt', 'w')
    
    for i in xrange(size):       
        arch.write(filesList[i]+'\n')
        
    arch.close()
    
    
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

    with open('narrativasSingleFile.txt', 'w') as f:
        f.write(text)  
        
def getIndexingALine ():
    cmd = 'aLine -i -l filesPathNarrativas.txt -d aLineNarrativas'
    os.system(cmd)
    
def getIndexingZettair ():
    cmd = '/usr/local/zettair/bin/zet -i narrativasSingleFile.txt'
    os.system(cmd)  

#################### STARTING THE SCRIPT ###########################

path = os.getcwd() # my actual path
pathDoc = path + '/narrativas.txt'  
fold = '/docs'
foldaLine = 'docsaLine/'
pathFiles = path + fold

processDocs (pathDoc, path)

#filesList = generateFilesPath (pathFiles,True)
filesList = glob.glob(pathFiles+'/*')
s = len(filesList)
getNFilesPath (filesList,s)

setSingleFile (filesList)







