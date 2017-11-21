#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Author: André Pacheco
Email: pacheco.comp@gmail.com

This class implements the naive bayes according to:

    
    
If you find some bug, please e-mail me =)
"""

import numpy as np
import sys
from scipy.stats import norm as gaussian

#sys.path.append('/home/patcha/Dropbox/Doutorado/Codigos/Python/utils/')

from utilsClassification import contErrorInt

class naiveBayes ():
    inTrain = None
    outTrain = None
    nLab = None
    stats = None
    
    def __init__ (self, inT, outT, nL):
        self.inTrain = inT
        self.outTrain = outT
        self.nLab = nL
        
        
    def splitByLabel (self):
        splited = dict()            
        for lb in xrange(1,self.nLab+1,1):
            splited[lb] = list()            
        
        for n in range(len(self.inTrain)):
            sam = self.inTrain[n]
            lab = int(self.outTrain[n][0])            
            splited[lab].append(sam)
            
        return splited
    
    def statsByLabel (self, splited):
        stats = dict()
        for i in xrange(len(splited)):
            samples = np.asarray(splited[i+1])
            samplesMean = samples.mean(axis=0)
            samplesStd = samples.std(axis=0)
            
            stats[i+1] = zip(samplesMean,samplesStd)
            
        self.stats = stats
        return stats
    
    def probByLabel (self, stats, inputData):
        probs = dict()
        for label, statsLabel in stats.iteritems():
            probs[label] = 1            
            for i in xrange(len(statsLabel)):
                labelMean, labelStd = statsLabel[i]
                probs[label] *= gaussian.pdf(inputData[i], labelMean, labelStd)
                
        return probs
    
    def getMaxProb (self, probs):
        predictedLabel = None
        maxProb = -1
        for label, prob in probs.iteritems():
            if prob > maxProb:
                predictedLabel = label
                maxProb = prob
        return predictedLabel

    def getSingle (self, stats, test):
        probs = self.probByLabel(stats,test)
        return self.getMaxProb(probs)

    def getResult (self, stats, testData, outReal):
        nSam = testData.shape[0]
        out = list()
        for i in xrange(nSam):
            probs = self.probByLabel(stats,testData[i])
            predLabel = self.getMaxProb(probs)
            out.append(predLabel)
            
            #print predLabel
            #print outReal[i]
            
        out = np.asarray(out, dtype=np.int32)
        out = np.reshape(out, (len(out),1))
        return contErrorInt(outReal, out)
        
        
        
            

           




