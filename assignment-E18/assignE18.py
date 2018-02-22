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
import re


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
        os.system('tar -xzf usielCarneiro.tar.gz -C '+ path)        
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
                fullText += p.text.encode('utf-8') + '\n'

            # Writing the .txt file
            arch = open (nameTxt, 'w')
            arch.write(fullText)
            arch.close()

def generatePDFs (filesList):
    ans = raw_input ('Do you wanna generate the PDF files? (It is going to take some time (y or n)? ')
    
    if ans == 'yes' or ans == 'y':
        print 'Generating the PDFs, please wait...'
        
        for fil in filesList:
            print 'Coverting the file: ', fil[59:]
            os.system ('doc2pdf ' + fil.replace(' ','\ '))
            
        return True
    
    return False
    
def generateHTML (filesList, pathName=None):
    if pathName is None:
        fileName = 'pagina.html'
    else:
        fileName = pathName
        
    arch = open(fileName, 'w')
    arch.write('<! DOCTYPE html> <html> 	<head> <meta charset=\"utf-8\"> <title> Arquivos Usiel Carneiro </title> </head>')
    arch.write('<h1 align=\"center\"> Lista dos arquivos escritos por Usiel Carneiro </h1> <hr> <body> <ul>')

    for fil in filesList:
        arch.write('<li> <p> <a align=\"center\" href=\"'+ fil +'\" target =\"_blank\" title =\"Abrir o arquivo\">'+ fil[59:] +'</a> </p> </li>')
        
    
    arch.write('</ul> </body> </html>')
    arch.close()
    
    
            
def getNGrams (path, amount=30):    
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

    print '**** Most frequency 2-grams ****'
    print '\n'.join('Gram: %s - Freq: %s' % x for x in freqTwoGrams.most_common(amount))
    print '\n**** Most frequency 3-grams ****'
    print '\n'.join('Gram: %s - Freq: %s' % x for x in freqThreeGrams.most_common(amount))


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
    print '**** Average of similarity between the docs pairwise: ', simi/len(sMat), ' *****'
    
    
    sMat = sMat[sMat[:,2].argsort()]
    n = sMat.shape[0]
    ns = 0
    mostSimi = list()
    included = list()
    for k in xrange(n-1,0,-1):
        t = (sMat[k][0], sMat[k][1])
        if (t[0] != t[1]) and ((t[1],t[0]) not in included):
            ns += 1
            included.append(t)
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
        w = aux[1].replace('”','').replace('“','').replace(' ','').replace('  ','').replace('‘','').replace('’','').replace(']','').replace('[','')
        if w in indexWords:            
            indexWords[w] += int(aux[2])
        else:
            indexWords[w] = int(aux[2])
    arch.close()
    return indexWords

# You cab get the most common: words, adjectives (adj) or nouns
def getMostCommon (indexWords, amount=30):    
    n = len(indexWords)
    most = indexWords.most_common(n)
    
    # Getting the most common words:
    print '\n**** The most common words ****'
    print '\n'.join('Word: %s - Freq: %s' % x for x in most[0:amount])
    
    
    # Getting the dictionary from my github
    if not os.path.isfile('dic-pt-br.txt'): 
        os.system ('wget https://raw.githubusercontent.com/paaatcha/dicionario-ptbr/master/dic-pt-br.txt')

    # Getting the most common adj and nouns:    
    sintatic = json.load(open("dic-pt-br.txt", 'r'))
    adj = list()
    nAdj = 0
    nouns = list()
    nNouns = 0
    for word in most:
        w = unicode(word[0],'utf-8').replace('"','')
        freq = word[1]
        try:
            if (sintatic[w] == 'adj.') and (nAdj < 30):
                nAdj +=1
                adj.append((w,freq))
            elif (sintatic[w] == 'm.' or sintatic[w] == 'f.') and (nNouns < 30):
                nNouns += 1
                nouns.append((w,freq))
        except KeyError:
            #print w
            pass
            
                
        if (nNouns > 30) and (nAdj > 30):
            break;

    print '\n**** The most common adjectives ****'    
    print '\n'.join('Word: %s - Freq: %s' % x for x in adj)
    
    print '\n**** The most common nouns ****'
    print '\n'.join('Word: %s - Freq: %s' % x for x in nouns)
        
def isDate (words):
    days = ('SEGUNDA', 'TERÇA', 'TERCA', 'QUARTA', 'QUINTA', 'SEXTA', 'SÁBADO', 'SABADO', 'DOMINGO')
    months = ('JANEIRO', 'FEVEREIRO', 'MARÇO', 'MARCO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO')
    prob, day, month = 0.0, None, None
    words = words.replace('/',' ').replace(',','').replace('\\',' ').replace('\n','').split(' ')
    siz = len(words)
    for w in words:            
        if w.upper() in days:
            day = w
            prob += 1.0
        if w.upper() in months:            
            month = w
            prob += 1.0
    
    prob /= siz
    return prob > 0.1, day, month
  
def isTitle (words):
    #p,_,_= isDate (words)
    return (len(words) <= 100 and len(words) > 3 )
    

def isVers (words):    
    bibleBooks = ('gênesis', 'genesis', 'êxodo', 'exodo', 'levítico', 'levitico', 'números', 'numeros', 'deuteronômio',\
    'deuteronomio', 'josué', 'josue', 'juizes', 'juízes', 'rute', 'samuel', 'reis', 'cronicas', 'crônicas', 'esdras',\
    'neemias', 'ester', 'jo', 'jó',  'salmos', 'proverbios', 'provérbios', 'eclesiastes', 'cantico', 'cântico',\
    'salomao', 'salomão', 'isaias', 'isaías',  'jeremias', 'lamentacoes', 'lamentações', 'ezequiel', 'daniel',\
    'oseias', 'joel', 'amós', 'amos', 'obadias', 'jonas', 'miqueias', 'naum', 'habacuque', 'sofonias', 'ageu',\
    'zacarias', 'malaquias', 'mateus', 'marcos', 'lucas', 'joão', 'joao', 'romanos', 'coríntios', 'corintios',\
    'gálatas', 'galatas', 'efésios', 'efesios',  'filipenses', 'colossenses', 'tessalonicenses', 'timóteo',\
    'tito', 'filêmon', 'filemon', 'hebreus', 'tiago', 'pedro', 'judas', 'apocalipse')
    
    abrev = ('1Co','1Cr','1Jo','1Pe','1Rs','1Sm','1Tm','1Ts','2Co','2Cr','2Jo','2Pe','2Rs','2Sm','2Tm','2Ts',\
    '3Jo','Ag','Am','Ap','At','Cl','Ct','Dn','Dt','Ec','Ed','Ef','Ex','Ez','Fm','Fp','Gl','Gn','Hb','Hc','Is',\
    'Jd','Jl','Jn','Jo','Jó','Jr','Js','Jz','Lc','Lm','Lv','Mc','Ml','Mq','Mt','Na','Ne','Nm','Ob','Os','Pv',\
    'Rm','Rt','Sf','Sl','Tg','Tt','Zc')    
    
    okSize = len(words) < 300    
    vers = re.findall('\([^)]+\)',words)
    
    okBook = False
    for v in vers:
        book = v.replace('(','').replace(')','').split(' ')[0].lower()
        if book in bibleBooks or book in abrev:
            okBook = True
        
    return okBook and okSize
    


def isText (words):
    pass
        
def splitPatterns (path, pathNew, verbose=False):  
    
    date, title = None, None
    
    
    with open(path,'r') as f:
        lines = f.readlines()
        
    k = 0
    while(k < len(lines)):
        newText = ''
        ok = False
        # Checking the date
        p, d, m = isDate(lines[k])
        if p:       
            newText += '<DATA_DO_DOCUMENTO>\n' + lines[k]
            
            # Go forward and find the title
            k += 1
            p = isTitle (lines[k])
            if p:
                newText += '\n<TITULO_DO_DOCUMENTO>\n' + lines[k]
                title = lines[k]                
                
                # Go forward and find the bible citation
                k += 1
                p = isVers (lines[k])
                if p:
                    newText += '\n<CITACAO_DA_BIBLIA>\n' + lines[k]
                
                    # Go forward and find the bible citation
                    k += 1
                    newText += '\n<TEXTO_DO_PASTOR>\n' + lines[k]
                    ok = True
            
        if ok:
            if m is not None:                
                pathFolder = pathNew + '/' + m            
                pathName = pathFolder + '/' + title[:-1] + '.txt'            
                if verbose:                                
                    print newText           
                    print pathNew
                    print pathName
                    
                isDir = os.path.isdir(pathFolder)
                if not isDir:
                    os.mkdir(pathFolder)         
                
                with open(pathName, 'w') as f:
                    f.write(newText)
        # Getting a new line
        k += 1
            
    




#################### STARTING THE SCRIPT ###########################

path = os.getcwd() # my actual path
pathFiles = path + '/usielCarneiro'  

# Cheking the database and download it if needsOUTBRO
checkingDataset (pathFiles)

# Getting the docx paths
filesListDocx = generateFilesPath (pathFiles, fileFormat='docx')

# Converting the docx to txt
#docx2txt(filesListDocx)

# Getting the txt paths
filesListTxt = generateFilesPath (pathFiles, fileFormat='txt')
n = len(filesListTxt)

# Writting the file of paths
pathFiles = writeNFilesPath (filesListTxt,n,'Usiel')

# Getting the n-grams
#getNGrams (pathFiles, 30)

for files in filesListTxt:
    splitPatterns (files, path, False)


