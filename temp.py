# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from agents import *

class BlindDog(Agent):
    
    def __init__(self, nome, programa=None):
        super().__init__(programa)
        self.nome=nome
        
    @property
    def nome(self) :
        return self.__nome
    @nome.setter
    def nome(self,nome) :
        self.__nome = nome
        
    def movedown(self):
        self.location += 1
    
    def eat(self, thing):
        '''returns True upon success or False otherwise'''
        if isinstance(thing, Food):
            print("Dog: Ate food at {}.".format(self.location))
            return True
        return False
    
    def drink(self, thing):
        ''' returns True upon success or False otherwise'''
        if isinstance(thing, Water):
            print("Dog: Drank water at {}.".format(self.location))
            return True
        return False

    def __str__(self) :
        return self.nome

        
class Food(Thing):
    def __str__(self):
        return "C"

class Water(Thing):
    def __str__(self):
        return "A"

class Park(Environment):
    
    def percept(self, agent):
        '''prints & return a list of things that are in our agent's location'''
        things = self.list_things_at(agent.location)
        print("{}:{}".format(agent.nome,list(map(str,things))))  ## exercício 3/4
        return things
    
    def execute_action(self, agent, action):
        '''changes the state of the environment based on what the agent does.'''
        if action == "move down":
            agent.movedown()
        elif action == "eat":
            items = self.list_things_at(agent.location, tclass=Food)
            if len(items) != 0:
                if agent.eat(items[0]): #Have the dog pick eat the first item
                    self.delete_thing(items[0]) #Delete it from the Park after.
        elif action == "drink":
            items = self.list_things_at(agent.location, tclass=Water)
            if len(items) != 0:
                if agent.drink(items[0]): #Have the dog drink the first item
                    self.delete_thing(items[0]) #Delete it from the Park after.
                    
    def is_done(self):
        '''By default, we're done when we can't find a live agent, 
        but to prevent killing our cute dog, we will or it with when there is no
        more food or water'''
        no_edibles = not any(isinstance(thing, Food) or isinstance(thing, Water) \
                             for thing in self.things)
        dead_agents = not any(agent.is_alive() for agent in self.agents)
        return dead_agents or no_edibles
    
    def __str__(self):
        dic = {}
        for x in self.things:
            loc = x.location
            dic[loc] = dic.get(loc, '')+str(x)
        if len(self.things) > 0 :
            max_loc = max([x.location for x in self.things])
        else :
            max_loc = -1
        mapa = str()
        for i in range(max_loc + 1) :
            mapa += "{}: {}\n".format(i,dic.get(i,""))
        return str(mapa)
    
class Park2D(XYEnvironment):
    
    def __init__(self,X,Y):
        super().__init__(X,Y)
    
    def execute_action(self, agent, action):
        if action == "move down":
            agent.movedown()
        elif action == "eat":
            items = self.list_things_at(agent.location, tclass=Food)
            if len(items) != 0:
                if agent.eat(items[0]): #Have the dog pick eat the first item
                    self.delete_thing(items[0]) #Delete it from the Park after.
        elif action == "drink":
            items = self.list_things_at(agent.location, tclass=Water)
            if len(items) != 0:
                if agent.drink(items[0]): #Have the dog drink the first item
                    self.delete_thing(items[0]) #Delete it from the Park after.
                    
    def __str__(self):
        dic = {}
        for x in self.things:
            loc = x.location
            dic[loc] = dic.get(loc, '')+str(x)
        print (dic)
        mapa = []
        for i in range(self.x_end) :
            mapa.append([i])
            for x in range(self.y_end):
                mapa.append((str(i),dic.get((i,x)," ")))
        return str(mapa)
    
        
def comportamento_do_cao(percepcao):
    '''Devolve uma acção em função da percepção'''
    if percepcao == [] :
        accao = 'move down'
    elif isinstance(percepcao[0],Food) :
        accao = 'eat'
    elif isinstance(percepcao[0],Water) :
        accao = 'drink'
    else :
        accao = comportamento_do_cao(percepcao[1:]) 
    return accao

    parque = Park2D(6,6)
    dog1 = BlindDog("*",comportamento_do_cao)
    dog2 = BlindDog("@",comportamento_do_cao)
    dogfood = Food()
    water = Water()
    parque.add_thing(dog1, (1,2))
    parque.add_thing(dog2, (3,4))
    parque.add_thing(dogfood, (4,3))
    parque.add_thing(water, (4,1))
    print(parque)
