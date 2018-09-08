# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 17:34:39 2018

@author: joaop
"""
from search import *

class EstadoRobos :
    """Um estado do problema dos 2 jarros é um par de jarros, em que cada jarro
    é representado por um par (capacidade,quantidade).
    """
    def __init__(self,troca=((0,0),(0,0)),robo = [(2,1),(4,1),(1,3),(2,4),(4,4),(5,5)]) :
        i=0
        self.robo = robo
        for element in self.robo:
            if element == troca[0]:
                self.robo[i]=troca[1]
            i+=1
        
    def robo_preto(self,estado) :
        """Método para verificar se um dado jarro está cheio. 
        O número do jarro é 1 ou 2.
        """
        for element in self.robo:
            if estado == element:
                return True
        return False
    
    def procurar(self,estado):
        movimento=[]
        for elemento in self.robo:
            x = elemento[0]
            y = elemento[1]
            preto=[]
            preto2=[]
            x1=0
            y1=0
            x2=0
            y2=0
            while x>0 and x<6:
                x=x+1
                if (x,y)!=elemento:
                    if self.robo_preto((x,y)) == True:
                        preto.append((x-1,y))
            while y>0 and y<6:
                y=y+1
                if (elemento[0],y-1) != elemento:
                    if self.robo_preto((elemento[0],y)) == True:
                        preto2.append((elemento[0],y-1))
            for element in preto:
                elemento1=element
                x1 = element[0]-3
                y1 = element[1]-3
                if x1<0:
                    x1=x1*-1
                if y1<0:
                    y1=y1*-1
            for element in preto2:
                elemento2=element
                x2 = element[0]-3
                y2 = element[1]-3
                if x2<0:
                    x2=x2*-1
                if y2<0:
                    y2=y2*-1
            if len(preto)==0 and len(preto2)!=0:
                movimento.append((elemento,elemento2))
            elif len(preto2)==0 and len(preto)!=0:
                movimento.append((elemento,elemento1))    
            elif len(preto2)!=0 and len(preto)!=0:
                distancia2 = x2+y2
                distancia1 = x1+y1
                if distancia1 >= distancia2:
                    movimento.append((elemento,elemento2))
                movimento.append((elemento,elemento1))
        return movimento
          
    def in_bounds(self,estado) :
        """Método para verificar se um dado jarro está vazio. 
        O número do jarro é 1 ou 2.
        """
        if estado[0]>=1 and estado[0]<= 5:
            if estado[1]>=1 and estado[1]<= 5:
                return True
        return False
    
    def __str__(self) :
        return str(self.robo)
    
    def __eq__(self,estado) :
        """Definir em que circunstância os dois estados são considerados iguais.
        Necessário para os algoritmos de procura em grafo.
        """
        if self.robo[0] == estado.robo[0] and self.robo[1] == estado.robo[1]:
            return estado
        
    def __hash__(self) :
        """Necessário para os algoritmos de procura em grafo."""
        return hash((self.robo[0],self.robo[1]))
    
    
class ProblemaRobos(Problem) :

    def __init__(self,inicial = EstadoRobos(), colocado_em = (3,3)) :
        super().__init__(inicial)
        self.colocado_em = colocado_em
           
    def goal_test(self,estado) :
        """Um estado é final se um dos seus jarros tiver uma quantidade igual
        àquela que se pretende medir.
        """
        return estado.robo[0][0] == self.colocado_em[0] and \
               estado.robo[0][1] == self.colocado_em[1] 
               
    def actions(self,estado) :
        accoes = [(10,(10,10))]
        move = estado.procurar(estado)
        for elemento in move:
            x = elemento[1][0]-3
            y = elemento[1][1]-3
            if x<0:
                x=x*-1
            if y<0:
                y=y*-1
            distancia = x+y
            for element in accoes:
                if distancia < element[0]:
                    accoes.remove(element)
                    accoes.append((distancia,elemento))
        return accoes
    
    def result(self,estado,acao) :
        resultante = EstadoRobos(acao[1])
        return resultante
    
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        print (str(c)+"\n",str(state1)+"\n",str(action)+"\n",str(state2)+"\n")
        return c + 1
    
    def h1(self,no) : 
        """Uma heurística é uma função de um estado.
        Nesta implementação, é uma função do estado associado ao nó
        (objecto da classe Node) fornecido como argumento.
        """
        h = {'[(2, 1), (4, 1), (1, 3), (2, 4), (4, 4), (5, 5)]':3,
               '[(2, 3), (4, 1), (1, 3), (2, 4), (4, 4), (5, 5)]':1,
               '[(2, 3), (4, 3), (1, 3), (2, 4), (4, 4), (5, 5)]':1,
               '[(3, 3), (4, 3), (1, 3), (2, 4), (4, 4), (5, 5)]':0}
        return h[str(no.state)]
    
prob_robos = ProblemaRobos()
print(prob_robos.initial)
print(prob_robos.colocado_em)

medida1 = greedy_best_first_graph_search(prob_robos,prob_robos.h1)
print(medida1.solution(),medida1.path_cost)
