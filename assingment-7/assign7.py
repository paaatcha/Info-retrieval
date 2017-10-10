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
from reportlab.pdfgen import canvas

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
        print 'The database has been already downloaded'

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

def generatePDF (text, pathName):
    c = canvas.Canvas(pathName)
    c.drawText0(text.encode('utf-8'))
    c.save()
    
            
def getNGrams (path):    
    arch = open(path,'r')
    allPaths = arch.readlines()
    arch.close()    
    print '**** Getting the N-grams ****'
    
       
   
    for pa in allPaths:        
        arch = open (pa[:-1],'r')
        sentence = arch.read()     
        twoGrams = ngrams(sentence.replace('"','').replace(',','').replace('.','').replace(':','').replace(';','').replace('!','').replace('?','').lower().split(),2)
        threeGrams = ngrams(sentence.replace('"','').replace(',','').replace('.','').replace(':','').replace(';','').replace('!','').replace('?','').lower().split(),3)

        freqTwoGrams = Counter(twoGrams)
        freqThreeGrams = Counter(threeGrams)
        arch.close()
        #break
    print '**** Most frequency 2-grams ****'
    print '\n'.join('Gram: %s - Freq: %s' % x for x in freqTwoGrams.most_common(5))
    print '\n**** Most frequency 3-grams ****'
    print '\n'.join('Gram: %s - Freq: %s' % x for x in freqThreeGrams.most_common(5))


def getSimilarityALine ():    
    cmd = 'aLine --similarity -d aLineUsielSimi --features aLineUsiel/cache.txt'
    os.system(cmd)

def getIndexingALine ():
    cmd = 'aLine -i -l filesPathUsiel.txt -d aLineUsiel'
    os.system(cmd)


def getSpaceDensity (filesList, amount=5):    
    sMat = np.loadtxt('similaridade.mtx', skiprows=2)
    simi = sum(sMat[:,2])
    print '\n**** Space density: ', simi-176, ' ****'
    sMat = sMat[sMat[:,2].argsort()]
    n = sMat.shape[0]
    ns = 0
    mostSimi = list()
    for k in xrange(n-1,0,-1):
        if sMat[k][0] != sMat[k][1]:
            ns += 1
            mostSimi.append(sMat[k][:])
            if ns == amount:
                break
    print '\n*** The most similarities files***'
    for k in mostSimi:
        print '--- Similarity: ', k[2], ' ---'
        print 'File 1: ', filesList[int(k[0])][59:]
        print 'File 2: ', filesList[int(k[1])][59:]        
        print '\n'

def getDictionaryALine (path):
    arch = open(path,'r')
    indexWords = Counter()
    for line in arch.readlines():
        aux = line.split()
        indexWords[aux[1]] = int(aux[2])
        
    arch.close()
    return indexWords

# You cab get the most common: words, adjectives (adj) or nouns
def getMostCommon (indexWords, amount=30):    
    n = len(indexWords)
    most = indexWords.most_common(n)
    
    # Getting the most common words:
    print '\n**** The most common words ****'
    print '\n'.join('Word: %s - Freq: %s' % x for x in most[0:amount])
    
    # Getting the most common adj and nouns:    
    sintatic = json.load(open("sintatic-pt-br.txt", 'r'))
    adj = list()
    nAdj = 0
    nouns = list()
    nNouns = 0
    for word in most:
        w = unicode(word[0],'utf-8').replace('"','')
        freq = word[1]
        try:
            if (sintatic[w] == 'ADJ') and (nAdj < 30):
                nAdj +=1
                adj.append((w,freq))
            elif (sintatic[w][0] == 'N') and (nNouns < 30):
                nNouns += 1
                nouns.append((w,freq))
        except KeyError:
            pass
            #print w
                
        if (nNouns > 30) and (nAdj > 30):
            break;

    print '\n**** The most common adjectives ****'    
    print '\n'.join('Word: %s - Freq: %s' % x for x in adj)
    
    print '\n**** The most common nouns ****'
    print '\n'.join('Word: %s - Freq: %s' % x for x in nouns)
        
        


#################### STARTING THE SCRIPT ###########################

path = os.getcwd() # my actual path
pathFiles = path + '/usielCarneiro'  

# Cheking the database and download it if needs
checkingDataset (pathFiles)

# Getting the docx paths
filesList = generateFilesPath (pathFiles, fileFormat='docx')

# Converting the docx to txt
docx2txt(filesList)

# Getting the txt paths
filesList = generateFilesPath (pathFiles, fileFormat='txt')
n = len(filesList)

# Writting the file of paths
pathFiles = writeNFilesPath (filesList,n,'Usiel')

# Getting the n-grams
getNGrams (pathFiles)


##############################  aLINE  ####################################
getIndexingALine()
getSimilarityALine()  


############################# The rest of metrics ########################
indexWords = getDictionaryALine (path+'/aLineUsiel/dictionary.txt')
getMostCommon (indexWords)
getSpaceDensity (filesList)




