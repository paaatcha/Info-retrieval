# -*- coding: utf-8 -*-
"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Autor: André Pacheco
% Email: pacheco.comp@gmail.com
% Essa função implementa o algoritmo genético (GA). Para setar a função objetivo edite o arquivo
% FuncaoObjetivo.m; Além disso, este código considera como critério de parada apenas o número de 
% iteração. Para verificar o um erro mínimo, basta adicionar um if-break no loop principal.
% 
% Entradas: 
%	dim = dimensão do problema
% 	nPop = tamanho da população
% 	vInit = Intervalado de inicialização: [-32 32] por exemplo
% 	nIter = numero de iterações
%       
%
% Saída:
%   melhor = Melhor valor encontrado da otimização
%   pos_   = Individuos que geraram o melhor valor 
%   todos_melhores = Histórico da otimização
%
%
%   Este código é aberto para fins acadêmicos, mas lembre-se, caso utilize:
%   dê crédito a quem merece crédito. Qualquer erro encontrado, por favor, 
%   reporte via e-mail para que possa corrigi-lo.
%   Faça bom uso =)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

import numpy as np


######################## INCLUDE THE FITNESS FUNCTION HERE ####################
def fitness_function (data):
    n = data.shape[0]-1
    sum_x = 0
    prod_cos = 1
    
    for i in xrange(n):
        sum_x += data[i] ** 2
        prod_cos *= np.cos((data[i]/np.sqrt(i+1))) 
    
    return (sum_x/4000) - prod_cos + 1
    


def GA (dim, nPop, vInit=(-15,15), nInt=100, cross_rate=0.65, mut_rate=0.1, mi=0, sigma=1, fit_func=None, params=None):
    
#    population = np.random.randint(vInit[0], vInit[1],(nPop, dim+1))    
    population = np.random.rand(nPop, dim+1)*vInit[1]
    all_best = np.zeros((nInt,1))    
       
    # just for initialization
    best = fitness_function (population[0]) 
    best_pos = 0   

    for i in xrange(nInt):
        best, best_pos, population = fitness(population, nPop, dim, best, best_pos, fit_func, params)
        new_pop = selection(population, nPop, dim)
        population = crossover(new_pop, nPop, dim, cross_rate, mi, sigma)
        population = mutation (population, nPop, dim, mut_rate, mi, sigma)
        all_best[i] = best
  
    return population[best_pos], best
    
    
def fitness (population, nPop, dim, best, best_pos, fit_func, params):
    for i in xrange(nPop):
        if fit_func is None:
            fit = fitness_function (population[i])            
        else:
            fit = fit_func(population[i], params)   
            
        if fit < best:
            best = fit
            best_pos = i
        
        population[i, dim] = fit
    return best, best_pos, population    
        
def selection (population, nPop, dim):
    new_pop = np.zeros_like(population)    
    
    for i in xrange(nPop):
        alet1 = np.random.randint(0,nPop)
        alet2 = np.random.randint(0,nPop)
        
        if population[alet1, dim] < population[alet2,dim]:
            new_pop[i] = population[alet1]
        else:
            new_pop[i] = population[alet2]
    
    return new_pop
    
def crossover (population, nPop, dim, cross_rate, mi, sigma):
    new_pop = np.zeros_like(population)
    for i in xrange(nPop-1):
        prob = np.random.rand()
        alet1 = np.random.randint(0,nPop)
        alet2 = np.random.randint(0,nPop)
        beta = np.random.normal(mi,sigma)
        
        if prob <= cross_rate:
            new_pop[i] = beta*population[alet1] + (1-beta)*population[alet2]
            new_pop[i+1] = (1-beta)*population[alet1] + (beta)*population[alet2]
        else:
            new_pop[i] = population[alet1]
            new_pop[i+1] = population[alet2]
            
    return new_pop
            
def mutation (population, nPop, dim, mut_rate, mi, sigma):
    for i in xrange(nPop):
        prob = np.random.rand()
        if prob <= mut_rate:
            beta = np.random.normal(mi,sigma)
            population[i] = population[i] * beta
            
    return population
        
    

#def test (data, params):
#    n = data.shape[0]-1    
#    sum_x = 0
#    prod_cos = 1
#    
#    for i in xrange(n):
#        sum_x += data[i] ** 2
#        prod_cos *= np.cos((data[i]/np.sqrt(i+1))) 
#    
#    return (sum_x/4000) - prod_cos + 1    


#a,b = GA (4,10,vInit=(0,5))            
#print a, b
    
    
    
    
    
    
    
    
    
    
    
    
        

    
    
    
    