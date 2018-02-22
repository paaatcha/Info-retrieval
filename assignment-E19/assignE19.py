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
import numpy as np
from time import time
import subprocess
            
            
def getPDFsPath (path):
    allPdfs = glob.glob(path+'/*.pdf')
    return allPdfs

    
# TODO    
def checkingDataset (path):     
    # checking if the files was downloaded    
    isDown = os.path.isdir(path)
       
    # Downloading the directory if it does not exist
    if (not isDown): 
        print 'Downloading the Tribuna database...'
        os.system('wget http://rii.lcad.inf.ufes.br/repositorioUFES.tar.gz')    
        os.system('mkdir repositorio-ufes')
        print 'Extracting the repositorio-ufes database...'
        os.system('tar -xzf repositorioUFES.tar.gz -C repositorio-ufes')        
        os.system('rm -rf repositorioUFES.tar.gz')
        print 'The files have been set'
    else:
        print 'The database has already downloaded'    

def checkPDFMiner ():
    # checking if the files was downloaded    
    isDown = os.path.isdir('PDFMiner')
    
    if not isDown:
        print 'Downloading and installing PDFMiner...'
        os.system('wget https://pypi.python.org/packages/57/4f/e1df0437858188d2d36466a7bb89aa024d252bd0b7e3ba90cbc567c6c0b8/pdfminer-20140328.tar.gz')    
        os.system('mkdir PDFMiner')        
        os.system('tar -xzf pdfminer-20140328.tar.gz -C PDFMiner')        
        os.system('rm -rf pdfminer-20140328.tar.gz')
        #os.system('python PDFMiner/setup.py install')
        print 'The files have been set'
    else:
        print 'PDFMiner has already installed'
    

def formatText (text):
    return text.replace('\n','').replace(',','').replace(':','').replace(';','').replace('.','').lower().split(' ')
    

    
def probDiss (word):
    wGeral = ('cdu', 'resumo', 'abstract', 'tese', 'orientador', 'orientadora', 'palavras-chave', 'key-words', 'keywords', 'co-orientador', 'co-orientadora', 'membro', 'dedicatória', 'agradecimentos', 'banca', 'examinadora', 'aprovada')
    wDiss = ('dissertação', 'mestrado', 'mestre')   

    k=0
    if word in wGeral:            
#        print word
        k=1
    elif word in wDiss:
#        print word
        k=3        
    return k
    
def probTese (word):
    wGeral = ('cdu', 'resumo', 'abstract', 'tese', 'orientador', 'orientadora', 'palavras-chave', 'chave', 'key', 'key-words', 'keywords', 'co-orientador', 'co-orientadora', 'membro', 'dedicatória', 'agradecimentos', 'banca', 'examinadora', 'aprovada')
    wTese = ('tese', 'doutorado', 'doutor')   

    k=0
    if word in wGeral:            
#        print word
        k=1
    elif word in wTese:
#        print word
        k=3        
    return k    
    
def probArtigo (word):
    wGeral = ('palavras-chave', 'chave', 'key', 'key-words', 'keywords', 'resumo', 'abstract', 'publicado', 'publicação')
    wArt = ('doi', 'correponding')   

    k=0
    if word in wGeral:            
#        print word
        k=1
    elif word in wArt:
#        print word
        k=3        
    return k        
    
def probLivro (word):
    wGeral = ('cdu', 'biblioteca', 'editorial', 'editora', 'revisão')
    wLiv = ('isbn', 'livro', 'edufes', 'diagramação')   

    k=0
    if word in wGeral:            
#        print word
        k=1
    elif word in wLiv:
#        print word
        k=3        
    return k    
    
def probabilities (words, verbose=False):
    kDiss, kTese, kArt, kLiv = 0, 0, 0, 0
    for w in words:
        kDiss+=probDiss(w)    
        kTese+=probTese(w)
        kArt+=probArtigo(w)
        kLiv+=probLivro(w)        
    
    wLen = len(words)
    if wLen>1000:
        kArt+=10   
    
    if verbose:
        print 'Diss: {} | Tese: {} | Artigo: {} | Livro: {}'.format(kDiss, kTese, kArt, kLiv)
        print 'Len: {}'.format(len(words))    
    
    v = np.array([kDiss, kTese, kArt, kLiv])
    res = v.argmax()
    if res==0:
        return 'DISS'
    elif res==1:
        return 'TESE'
    elif res==3:
        return 'LIV'
    else:
        return 'ART'
        
def generateHTML (data, pathName=None):
    if pathName is None:
        fileName = 'pagina.html'
    else:
        fileName = pathName
        
    arch = open(fileName, 'w')
    arch.write('<! DOCTYPE html> <html> 	<head> <meta charset=\"utf-8\"> <title> Repositório UFES </title> </head>')
    arch.write('<h1 align=\"center\"> Lista dos arquivos existentes no repositório UFES </h1> <hr> <body> <ul>')

    for key in data.keys():
        if key == 'DISS':
            n = len(data[key])
            arch.write('<h3 align=\"center\"> Dissertações de mestrado ('+str(n)+' arquivos) </h3> <hr>')
        elif key == 'TESE':
            n = len(data[key])
            arch.write('<h3 align=\"center\"> Teses de doutorado ('+str(n)+' arquivos) </h3> <hr> <body>')
        elif key == 'ART':
            n = len(data[key])
            arch.write('<h3 align=\"center\"> Artigos ('+str(n)+' arquivos) </h3> <hr> <body>')
        elif key == 'LIV':
            n = len(data[key])
            arch.write('<h3 align=\"center\"> Livros ('+str(n)+' arquivos) </h3> <hr> <body>')

        arch.write('<body> <ul> ')
        for fil in data[key]:
            name = fil.split('/')[-1][0:-4]            

                
            arch.write('<li> <p> <a align=\"center\" href=\"'+ fil +'\" target =\"_blank\" title =\"Abrir o arquivo\">'+ name +'</a> </p> </li>')
        
        arch.write('</ul>')
        
    arch.write('</body> </html>')
    arch.close()      

def PDFClassification (paths):
    
    repo = dict()
    repo['DISS'] = list()
    repo['TESE'] = list()
    repo['LIV'] = list()
    repo['ART'] = list()    
#    p = '/home/labcin/AndrePacheco/info-retrieval/assingment-E10/repositorio-ufes/documentos/10-852.pdf'
    
    n = len(paths)
    k = 1
#    paths = paths[0:100]
    for p in paths:
        print 'Loading PDF {} of {}'.format(k,n)
        k+=1
        
        
        cmd = 'pdf2txt.py -P "" -m 4 '+ p 
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        text, err = proc.communicate()            

        words = formatText(text)
        label = probabilities (words)
        
        repo[label].append(p)
            
        
        generateHTML (repo, 'repositorio-ufes.html') 



#################### STARTING THE SCRIPT ###########################

path = os.getcwd() # my actual path
pathRepo = path + '/repositorio-ufes/documentos'

checkingDataset (path+'/repositorio-ufes')
pathsPDFs = getPDFsPath(pathRepo)

PDFClassification(pathsPDFs)    


#print text






