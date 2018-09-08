# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 21:31:46 2018

@author: joaop
"""

from search import *



class ProblemaTeoricas_1(Problem) :
    grafo = {'I':[('A',2),('B',5)],
             'A':[('C',2),('D',4),('I',2)],
             'B':[('D',1),('F',5),('I',5)],
             'C':[],
             'D':[('C',3),('F',2)],
             'F':[]}

    def actions(self,estado) :
        sucessores= ''
        for element in self.grafo[estado]:
            sucessores += element[0]
        print (sucessores)
        accoes = map(lambda x : "ir de {} para {}".format(estado,x),sucessores)
        print (accoes)
        return list(accoes)


    def result(self, estado, accao) :
        """Assume-se que uma acção é da forma 'ir de X para Y'
        """
        return accao.split()[-1]
    
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        i=-1
        for element in self.grafo[state1]:
            print (element[0], state2)
            if element[0] == state2:
                i+=1
                print (c + self.grafo[state1][i][1])
                return c + self.grafo[state1][i][1]
            
    def h2(self,no) : 
        """Uma heurística é uma função de um estado.
        Nesta implementação, é uma função do estado associado ao nó
        (objecto da classe Node) fornecido como argumento.
        """
        h = {'I':7, 'A':2,'B':3,'C':1,'D':5,'F':0}
        return h[no.state]
    
    def h1(self,no) : 
        """Uma heurística é uma função de um estado.
        Nesta implementação, é uma função do estado associado ao nó
        (objecto da classe Node) fornecido como argumento.
        """
        h = {'I':4, 'A':3,'B':2,'C':2,'D':1,'F':0}
        return h[no.state]
    
    def h1(self,estado) : 
        """Uma heurística é uma função de um estado.
        Nesta implementação, é uma função do estado associado ao nó
        (objecto da classe Node) fornecido como argumento.
        """
        heuristica = estado[0]+estado[1]
        
        h = {'I':4, 'A':3,'B':2,'C':2,'D':1,'F':0}
        return h[no.state]
        
        
problema_1 = ProblemaTeoricas_1('I','F')     
medida1 = uniform_cost_search(problema_1)
print(medida1.solution())
print(medida1.path())    

res_astar = astar_search(prob1,prob1.h1)
print(res_astar.solution(),res_astar.path_cost)

prob1 = ProblemaTeoricas_1('I','F') 
res_gbfs = greedy_best_first_graph_search(prob1,prob1.h1)
print(res_gbfs.solution(),res_gbfs.path_cost)
        
    
class EstadoJarros :
    """Um estado do problema dos 2 jarros é um par de jarros, em que cada jarro
    é representado por um par (capacidade,quantidade).
    """
    def __init__(self,jarros = ((3,0),(5,0))) :
        self.jarros = jarros
        
    def jarro_cheio(self,num) :
        """Método para verificar se um dado jarro está cheio. 
        O número do jarro é 1 ou 2.
        """
        capacidade, quantidade = self.jarros[num-1]
        return capacidade == quantidade
    
    def jarro_vazio(self,num) :
        """Método para verificar se um dado jarro está vazio. 
        O número do jarro é 1 ou 2.
        """
        _, quantidade = self.jarros[num-1]
        return quantidade == 0
    
    def __str__(self) :
        return str(self.jarros)
    
    def __eq__(self,estado) :
        """Definir em que circunstância os dois estados são considerados iguais.
        Necessário para os algoritmos de procura em grafo.
        """
        return self.jarros == estado.jarros
    
    def __hash__(self) :
        """Necessário para os algoritmos de procura em grafo."""
        return hash((self.jarros[0],self.jarros[1]))
    
class ProblemaJarros(Problem) :

    def __init__(self,inicial = EstadoJarros(), vamos_medir = 4) :
        super().__init__(inicial)
        self.vamos_medir = vamos_medir
    
    def actions(self,estado):
          accoes = list()
          if not estado.jarro_cheio(1) :
              accoes.append("encher jarro 1")
          if not estado.jarro_cheio(2) :
              accoes.append("encher jarro 2")
          if not estado.jarro_vazio(1) :
              accoes.append("esvaziar jarro 1")
          if not estado.jarro_vazio(2) :
              accoes.append("esvaziar jarro 2")
          if not estado.jarro_vazio(1) and not estado.jarro_cheio(2):
              accoes.append("verter de 1 para 2")
          if not estado.jarro_vazio(2) and not estado.jarro_cheio(1):
              accoes.append("verter de 2 para 1")
          return accoes

    def result(self,estado,acao) :
        cap1, quant1 = estado.jarros[0]
        cap2, quant2 = estado.jarros[1]

        if acao == "encher jarro 1" :
            resultante = EstadoJarros(((cap1,cap1),(cap2, quant2)))
        elif acao == "encher jarro 2" :
            resultante = EstadoJarros(((cap1,quant1),(cap2, cap2)))
        elif acao == "esvaziar jarro 1" :
            resultante = EstadoJarros(((cap1,0),(cap2, quant2)))
        elif acao == "esvaziar jarro 2" :
            resultante = EstadoJarros(((cap1,quant1),(cap2, 0)))
        elif acao == "verter de 1 para 2" :
            em2 = min(cap2,quant1+quant2)
            resultante = EstadoJarros(((cap1,quant1+quant2-em2),(cap2,em2)))
        elif acao == "verter de 2 para 1" :
            em1 = min(cap1,quant1+quant2)
            resultante = EstadoJarros(((cap1,em1),(cap2,quant1+quant2-em1)))
        else :
            raise "Há aqui qualquer coisa mal>> acao não reconhecida"
 
        return resultante
       
    def goal_test(self,estado) :
        """Um estado é final se um dos seus jarros tiver uma quantidade igual
        àquela que se pretende medir
        """
        return estado.jarros[0][1] == self.vamos_medir or \
               estado.jarros[1][1] == self.vamos_medir
 

        
