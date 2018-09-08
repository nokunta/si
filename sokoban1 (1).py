from search import *
import copy, math, time
import sys

k = 1

class Box:    
        def __init__(self, pos):
                self.x = pos[0]
                self.y = pos[1]                    
        
        def up(self):
               self.y -= 1   

        def down(self):
                self.y+=1

        def left(self):
                self.x-=1

        def right(self):
                self.x+=1

        def __gt__(self,estado):
            return (self.x,self.y) > (state.x,state.y)

        def __lt__(self,estado):
            return (self.x,self.y) < (state.x,state.y)

        def __eq__(self,estado):
            return self.x == estado.x and self.y == estado.y

        def __str__(self):
            return str((self.x,self.y))

        def __hash__(self):
            return hash(str(self))

class Wall:    
        def __init__(self, pos):
                self.x = pos[0]
                self.y = pos[1]                    
                
        def __str__(self):
            return str((self.x,self.y))
        
        def __eq__(self, state):
            return self.x == state.x and self.y == state.y
        
        def __gt__(self,estado):
            return (self.x,self.y) > (state.x,state.y)
        
        def __lt__(self, state):
            return (self.x,self.y) < (state.x,state.y)


        def __hash__(self):
            return hash(str(self))

class Player:
        def __init__(self, pos):
                self.x = pos[0]
                self.y = pos[1]

        def up(self):
                self.y-=1

        def down(self):
                self.y+=1

        def left(self):
                self.x-=1

        def right(self):
                self.x+=1
        
        def __str__(self):
            return str((self.x,self.y))

        def __hash__(self):
            return hash(str(self))

        def __lt__(self, state):
            return (self.x,self.y) < (state.x,state.y)

class Goal:
        def __init__(self, pos):
                self.x = pos[0]
                self.y = pos[1]
                
        def __str__(self):
            return str((self.x,self.y))

class Estado:
        WALL = "#"
        FREE = "."
        BOX = "*"
        TARGET = "o"
        SOKO = "A"
        BOX_IN = "@"
        SOKO_IN = "B"

        def __init__(self, wall = [],boxes=[],player=[],empty=[],targets=[],width=None,height=None,walls2 = [],boxes2= [],state =  []):
                self.can_move = []
                self.walls    = wall
                self.walls2 = walls2
                self.boxes    = boxes
                self.boxes2    = boxes2
                self.player   = player
                self.empty    = empty
                self.targets  = targets
                self.state    = state
                self.width    = width
                self.height   = height
                
  
                
        def __str__(self):
            coord = []
            #print ("++++++++++")
            #print (self.height, self.width)
            #print ("********")
            for i in range(self.height):
                for j in range(self.width):
                    coord.append((j,i))
            
            boxes = []
            for i in self.boxes:   
                boxes.append((i.x,i.y))
                
            targets = []
            for i in self.targets:   
                targets.append((i.x,i.y))
                

            mapa = ""
            k = 0
            for i in coord:
                if k%self.width == 0:
                    mapa += '\n'
                if i in boxes:
                    if i in targets:
                        mapa += "@"
                    else:
                        mapa += '*'
                
                elif i[0] == self.player[0].x and  i[1] == self.player[0].y:
                    if i in targets:
                        mapa += 'B'
                    else:
                        mapa += 'A'
                
                elif i in targets:
                    mapa += 'o'
                    
                elif i in self.walls:
                    mapa += "#"
                    
                elif i in self.empty:
                    mapa += "."
                    
                k+=1
                
            return mapa
                
                

        def read_map(self, file):
                lines = []
                with open(file) as f:
                        for line in f:
                                lines.append(line)
                walls   = []
                empty   = []
                boxes   = []
                targets = []
                player  = []
                walls2 = []
                boxes2 = [] 
                h = 0
                w = 0
                for i in range(len(lines)):
                    for j in range(len(lines[i])):
                        if lines[i][j] == "#":
                            wall2 = Wall((j,i))
                            walls2.append(wall2)
                            walls.append((j,i))
                            
                        if lines[i][j] == "A":
                            soko = Player((j,i))
                            player.append(soko)
                            self.can_move.append((j,i))

                        if lines[i][j] == ".":
                            empty.append((j,i))
                            self.can_move.append((j,i))

                        if lines[i][j] == "*":
                            box = Box((j,i))
                            boxes.append(box)
                            boxes2.append((j,i))
                            self.can_move.append((j,i))
                            
                        if lines[i][j] == "o":
                            target = Goal((j,i))
                            targets.append(target)
                            self.can_move.append((j,i))
                            
                        if lines[i][j] == "B":
                            soko = Player((j,i))
                            player.append(soko)
                            target = Goal((j,i))
                            targets.append(target)
                            self.can_move.append((j,i))
                            
                        if lines[i][j] == "@":
                            box = Box((j,i))
                            boxes.append(box)
                            target = Goal((j,i))
                            targets.append(target)
                            self.can_move.append((j,i))

                self.walls = walls
                self.walls2 = walls2
                self.boxes2 = boxes2
                self.boxes = boxes
                self.player = player
                self.empty = empty
                self.targets = targets
                self.state = walls+boxes+player+empty+targets+walls2+boxes2
                self.height =walls[-1][1]+1
                self.width = walls[-1][0]+1

        

        def surroundings(self, position):
                if position in self.walls:                    
                        return 'WALL'
                for i in self.boxes:
                    if position == (i.x,i.y):
                        return 'BOX'
                if position in self.empty:
                        return 'EMPTY'
                for i in self.targets:
                    if position == (i.x,i.y):
                        return 'TARGET'
                
        def surroundings2(self, position):
                if position in self.walls:                    
                        return 'WALL'
                for i in self.boxes:
                    if position == (i[0],i[1]):
                        return 'BOX'
                if position in self.empty:
                        return 'EMPTY'
                for i in self.targets:
                    if position == (i.x,i.y):
                        return 'TARGET'
                        

        def percept(self, player):
             things = {}
             things['up']    = self.surroundings((player.x,player.y-1))
             things['down']  = self.surroundings((player.x,player.y+1))
             things['left']  = self.surroundings((player.x-1,player.y))
             things['right'] = self.surroundings((player.x+1,player.y))
             return things
         
        def percept2(self, player):
             things = {}
             things['up']    = self.surroundings2((player[0],player[1]-1))
             things['down']  = self.surroundings2((player[0],player[1]+1))
             things['left']  = self.surroundings2((player[0]-1,player[1]))
             things['right'] = self.surroundings2((player[0]+1,player[1]))
             return things
         
        def __lt__(self, state):
            return self.player[0]<state.player[0] and set(self.boxes) <set(state.boxes)
                
        def __hash__(self):
            return hash(str(self))

        def __gt__(self, state):
            return self.player[0]> state.player[0] and set(self.boxes) >set(state.boxes)
        
        def __eq__(self, state):
            return str(self) == str(state)




class Sokoban(Problem):
        
        def __init__(self, initial, goal=None):
                super().__init__(initial)
                self.initial = initial
                self.goal = goal
                
                
        def goal(self, state):
            pass

        def actions(self, state):
                can_do = []
                actions = state.percept(state.player[0])
                for i in actions.keys():
                        if actions[i] == 'BOX':
                            box = self.box_to_move(state,i)
                            if self.next_to_box(state, i,box[0])==True:
                                can_do.append('push '+i)
                        if actions[i] == 'EMPTY':
                                can_do.append('move '+i)
                        if actions[i] == "TARGET":
                            can_do.append('move '+i)
                return can_do
    
        def goal_test(self, mapa):
            i=0
            alvos = len(mapa.targets)
            for caixa in mapa.boxes:
                for alvo in mapa.targets:
                    if (caixa.x, caixa.y) == (alvo.x, alvo.y):
                        i+=1
            if i==alvos:
                return True
            return False
        
        def next_to_box(self,state, move, thing):
            next = state.percept(thing)[move]
            if next == 'BOX' or next == "WALL":
                return False
            return True
        
        def push_box(self, state, move, pos):
            boxes = []
            for box in stae:
                if pos[0] == box.x and pos[1]==box.y:
                    if move == 'up':
                         boxes.append()
                    if move == 'down':
                        return (box.x,box.y+1)
                    if move == 'left':
                        return (box.x-1,box.y)
                    if move == 'right':
                        return (box.x+1,box.y)
                    
                    
        def box_to_move(self, state, action):
            player = state.player[0]
            boxes = []
            new_map = copy.deepcopy(state.boxes)
            for i in new_map:
                
                if action == 'up' and (player.x,player.y-1)==(i.x,i.y):
                    boxes.append((i))
                if action == 'down' and (player.x,player.y+1)==(i.x,i.y):
                    boxes.append((i))
                if action == 'left' and (player.x-1,player.y)==(i.x,i.y):
                    boxes.append((i))
                if action == 'right' and (player.x+1,player.y)==(i.x,i.y):
                    boxes.append((i))
            return boxes
            
        
        
        def result(self, state, move):
            new_box = state.boxes
            old_player = state.player[0]
            
            new_map = copy.deepcopy(state)
            player = new_map.player
            
            if move=="push up":
                new_box = self.box_to_move(state,'up')
                if self.next_to_box(new_map,'up',new_box[0]):
                    for i in new_box:
                        if (i.x,i.y) == (old_player.x,old_player.y-1):
                            old_box = new_map.boxes[0]
                            
                            new_map.empty.append((new_map.player[0].x,new_map.player[0].y))
                            
                            if new_map.percept((new_box[0]))["up"] == 'TARGET':
                                pass
                            else:
                                new_map.empty.remove(( new_map.player[0].x,new_map.player[0].y-2))

                            c=0
                            for i in new_map.boxes:
                                if (i.x,i.y) == (new_box[0].x,new_box[0].y):
                                    new_map.boxes[c].up()
                                c+=1
                            new_map.player[0].up()
                
                
            elif move=="push down":
                new_box = self.box_to_move(state,'down')
                if self.next_to_box(new_map,'down',new_box[0]):
                    for i in new_box:
                        if (i.x,i.y) == (old_player.x,old_player.y+1):
                            old_box = new_map.boxes[0]
                            new_map.empty.append((new_map.player[0].x,new_map.player[0].y))
                            if new_map.percept((new_box[0]))["down"] == 'TARGET':
                                pass
                            else:
                                new_map.empty.remove(( new_map.player[0].x,new_map.player[0].y+2))
                            c=0
                            for i in new_map.boxes:
                                if (i.x,i.y) == (new_box[0].x,new_box[0].y):
                                    new_map.boxes[c].down()
                                c+=1
                            new_map.player[0].down()
                            
                            
                        
            elif move=="push left":
                new_box = self.box_to_move(state,'left')
                if self.next_to_box(new_map,'left',new_box[0]):
                    for i in new_box:
                        if (i.x,i.y) == (old_player.x-1,old_player.y):
                            old_box = new_map.boxes[0]
                            new_map.empty.append((new_map.player[0].x,new_map.player[0].y))
                            if new_map.percept((new_box[0]))["left"] == 'TARGET':
                                pass
                            else:
                                new_map.empty.remove(( new_map.player[0].x-2,new_map.player[0].y))
                            c=0
                            for i in new_map.boxes:
                                if (i.x,i.y) == (new_box[0].x,new_box[0].y):
                                    #print(c)
                                    new_map.boxes[c].left()
                                c+=1
                            new_map.player[0].left()                            

            elif move=="push right":
                new_box = self.box_to_move(state,'right')
                if self.next_to_box(new_map,'right',new_box[0]):
                    for i in new_box:
                        if (i.x,i.y) == (old_player.x+1,old_player.y):
                            old_box = new_map.boxes[0]
                            new_map.empty.append((new_map.player[0].x,new_map.player[0].y))
                            if new_map.percept((new_box[0]))["right"] == 'TARGET':
                                pass
                            else:
                                #print(( new_map.player[0].x+2,new_map.player[0].y))
                                new_map.empty.remove(( new_map.player[0].x+2,new_map.player[0].y))
                            c=0
                            for i in new_map.boxes:
                                if (i.x,i.y) == (new_box[0].x,new_box[0].y):
                                    #print(c)
                                    new_map.boxes[c].right()
                                c+=1
                            new_map.player[0].right()
                            
            
            elif move == "move up":
                 if new_map.percept((new_map.player[0]))["up"] == 'TARGET':
                        new_map.empty.append((old_player.x ,old_player.y))
                 else:
                        new_map.empty.remove(( player[0].x ,player[0].y-1))
                        new_map.empty.append((old_player.x ,old_player.y))
                 new_map.player[0].up()
                            
                    
            elif move == "move down":
                if new_map.percept((new_map.player[0]))["down"] == 'TARGET':
                        new_map.empty.append((old_player.x ,old_player.y))
                else:
                        new_map.empty.remove(( player[0].x ,player[0].y+1))
                        new_map.empty.append((old_player.x ,old_player.y))
                new_map.player[0].down()
                    
            elif move == "move left":
                 if new_map.percept((new_map.player[0]))["left"] == 'TARGET':
                        new_map.empty.append((old_player.x ,old_player.y))
                 else:
                        new_map.empty.remove(( player[0].x-1 ,player[0].y))
                        new_map.empty.append((old_player.x ,old_player.y))
                 new_map.player[0].left()
                 
                    
            elif move == "move right":
                if new_map.percept((new_map.player[0]))["right"] == 'TARGET':
                        new_map.empty.append((old_player.x ,old_player.y))
                else:
                        new_map.empty.remove(( player[0].x +1,player[0].y))
                        new_map.empty.append((old_player.x ,old_player.y))
                new_map.player[0].right()
                        
                           
            aa =  Estado(new_map.walls, new_map.boxes,\
                          new_map.player, new_map.empty, new_map.targets,new_map.width,new_map.height,new_map.walls2,new_map.boxes2, new_map.state)
            global k
            k += 1
            return aa
                              
        def path_cost(self, c, state1, action, state2):
                if action.split(" ")[0]=="push":
                    c+=1
                else:
                    c+=2
                return c



        def h1(self,estado) : 
            """EVITAR CANTOS
            """
            f = 0
            walls =[]
            #print("$$$$$$$$$")
            for w in estado.state.walls:
                walls.append(w)
                
            targets = []
            for w in estado.state.targets:
                targets.append((w.x,w.y))
            for i in estado.state.boxes:
                    if (i.x-1,i.y) in walls and (i.x,i.y-1) in walls and (i.x,i.y) not in targets:
                        f+=50
                    elif (i.x-1,i.y) in walls and (i.x,i.y+1) in walls and (i.x,i.y) not in targets:
                        f+=50
                    elif (i.x+1,i.y) in walls and (i.x,i.y+1) in walls and (i.x,i.y) not in targets:
                        f+=50
                    elif (i.x+1,i.y) in walls and (i.x,i.y-1) in walls and (i.x,i.y) not in targets:
                        f+=50
                    else:
                        f-=500
            return f


        def h2(self,estado) : 
            """Uma heurística é uma função de um estado.
            Nesta implementação, é uma função do estado associado ao nó
            (objecto da classe Node) fornecido como argumento.
            """
            def dist(a,b):
                return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
            distance = []
            boxes = []
            for b in estado.state.boxes:
                boxes.append((b.x, b.y))
            targets = []
            for w in estado.state.targets:
                targets.append((w.x, w.y))

            for i in boxes:
                #box_dist = 10000
                for j in targets:
                    distance.append(dist(j, i))
            #print(distance)

            distance.sort()
            l =int(len(distance)/2)
            d = distance[:l]	
            s = sum(d)/2
            return s
        
        def h3(self,estado):
          '''ver se tem uma caixa em cima da target'''           
          count = 0
          for box in estado.state.boxes:
            if box not in estado.state.targets:
              count += 20
            else:
                count -= 20
          return count


        def h4(self,estado):
            f=0
            if estado.action != None:
                acao = estado.action.split(" ")
                if acao[0] == "push":
                    f-=20
                else:
                    f+=5
                    
            return f


        def h5(self, estado):
            def dist(a, b):
                return abs((a[0] - b[0])) + abs((a[1] - b[1]))

            distance = []
            boxes = []
            for b in estado.state.boxes:
                boxes.append((b.x, b.y))
            targets = []
            for w in estado.state.targets:
                targets.append((w.x, w.y))

            for i in boxes:
                for j in targets:
                    distance.append(dist(j, i))

            distance.sort()
            l =int(len(distance)/2)
            d = distance[:l]	
            s = sum(d)/2
            return s




a = Estado()
a.read_map('puzzle2.txt')
print (a.state)
b = Sokoban(a)
print("#############################")
start = time.time()
res_gbfs = best_first_graph_search(b,b.h4)
print(res_gbfs.solution())
print(k)
end = time.time()
print(end - start)

