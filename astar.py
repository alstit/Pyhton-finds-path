'''
Created on 26 janv. 2020

@author: User
'''


import pygame
from math import sqrt
from random import random, randint
import queue
from itertools import count

unique = count()


THICKNESS = 1
 

WIDTH = 100
HEIGHT = 100

SCREENWIDTH = 1000
SCREENHEIGHT = 1000



#node structure x,y = position, c = count to get to this position, d is distance to distination
class node:
    x = 0
    y = 0
    c = 0
    d = 0
    h = 0
    openList = 0
    isWall = 0
    previous = None
#openlist = 0 : not examined yet
#openlist = 2 <=> closed list
# node are defined by their position on map : i,j
    def __init__(self,i,j):
        self.x = i
        self.y = j
        self.c = 1000
        self.d = 1000
        self.h  = self.c + self.d
        self.isWall = 0
  
    # def __lt__(self, anode):
        # return 0
    # def __gt__(self, anode):
        # return 0

if __name__ == '__main__':
    


    print("live visualisation ?(y,n)")
    live = input()
    if live == "n":
        live = 0
    elif live == "y":
        live = 1
    else :
        print("default yes")
    
    
    # grid is the mqp to search
    grid = []
    
    # grid definition
    for i in range(HEIGHT):
        for j in range(WIDTH):
            grid.append(node(i,j))
    
      # size in pixel of each square on grid
    rectWidth = SCREENWIDTH / WIDTH
    rectHeight = SCREENHEIGHT / HEIGHT
    
    final = grid[80]
    
    x = None
    y = None

    
    pygame.init()
    display = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
    display.fill((255,255,255))
    
    #randomly place wall
    FLAG_inputOK = 0
    for i in range(WIDTH-15):
        grid[int(HEIGHT/2)+i*(WIDTH)].isWall =1


        

  # set a continuous wall in half of screen
    for i in range(WIDTH*HEIGHT - int((WIDTH*HEIGHT)/1.5)):
        grid[randint(0,len(grid)-1)].isWall = 1
    
    # first part, to select start and finish node
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                (x,y)=pygame.mouse.get_pos()
                
        
        if x != None and FLAG_inputOK == 0:
                for anode in grid:
                    if abs(anode.x*rectWidth - x) <= rectWidth + 1 and abs(anode.y*rectWidth - y )<= rectWidth +1:
                        anode.openList = 1
                        anode.isWall = 0
                        pygame.draw.rect(display,(0,255,0),(anode.x*rectHeight,anode.y*rectWidth,rectWidth,rectHeight))
                        FLAG_inputOK = 1
                        x = None
                        break

        elif FLAG_inputOK == 1 and x!= None :
            i = 0
            for anode in grid:
                if abs(anode.x*rectWidth - x) <= rectWidth + 1 and abs(anode.y*rectWidth - y )<= rectWidth +1:
                    final = grid[i]
                    final.isWall = 0
                    break
                i += 1
            break
        # display grid     
        for i in range(WIDTH):
            for j in range(HEIGHT):
                pygame.draw.rect(display, (0,0,0), (i*rectHeight,j*rectWidth,rectWidth,rectHeight), THICKNESS)
                
        pygame.display.flip()
               
                
    # selecting first node . Speed can be improve by not searching the whole grid array, as we could define the first current searching node at the start point selection 
    for anode in grid :
        if anode.openList == 1:
            current = anode 
    current.d = sqrt((current.x - final.x)**2+(current.y-final.y)**2)
    current.h = current.c + current.d

#LowestF is a priorityqueue which contain search in openlist with their heuristics
    lowestF = queue.PriorityQueue(maxsize = len(grid))
    lowestF.put((current.h,next(unique),current))
   
    
    while(True):
        
            #pygame.time.wait(50)
        if current.x == final.x and current.y == final.y :
            print("WON")
            break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
        #get higest priority element to search (lowest heuristics <=> closest to destination)
        elem = lowestF.get() 

        current=elem[2] 
        current.openList = 2
        
        # for anode in grid:
            # if anode.isWall == 1:
                # continue
            # if anode.x == current.x and anode.y == current.y:
                # anode.openList = 2
                
        

        
        index = grid.index(current)
        
        
        # get closest neighbor of current searched node
        closest = [None] *8
        
        closest[0]=( grid[index+1-WIDTH])
        closest[1]=(grid[index+1])
        closest[2]=(grid[index+1+WIDTH])
        closest[3]=(grid[index-WIDTH])
        closest[4]=(grid[index+WIDTH])
        closest[5]=(grid[index-WIDTH-1])
        closest[6]=(grid[index-1])
        closest[7]=(grid[index-1+WIDTH])


        #check neigboh heuristic, and add them to open list
        neighbor = []
        for anode in closest:
            if anode.isWall:
                continue
            if anode == current:
                continue
            #print(current.x,current.y)
            #print(anode.h)
            if anode.openList!=2:
                if anode.x == current.x + 1 and (anode.y == current.y or anode.y == current.y + 1 or anode.y == current.y - 1):

                    anode.c = current.c + 1
                    anode.d = sqrt((anode.x - final.x)**2+(anode.y-final.y)**2)
                    if anode.openList == 1 :
                        if anode.c + anode.d > anode.h:
                            continue
                    elif anode.openList == 0 :
                        anode.h = anode.c + anode.d 
                        anode.openList =1
                        lowestF.put((anode.h,next(unique),anode))
                    neighbor.append(anode)
                    
                if anode.x == current.x - 1 and (anode.y == current.y or anode.y == current.y + 1 or anode.y == current.y - 1):
                    anode.c = current.c + 1
                    anode.d = sqrt((anode.x - final.x)**2+(anode.y-final.y)**2)
                  
                    if anode.openList == 1 :
                        if anode.c + anode.d > anode.h:                    
                            continue
                    elif anode.openList == 0 :
                        anode.h =  anode.c + anode.d
                        anode.openList =1
                        lowestF.put((anode.h,next(unique),anode))                   
                    neighbor.append(anode)
                if anode.x == current.x and (anode.y == current.y + 1 or anode.y == current.y - 1):
                    anode.c = current.c + 1

                    anode.d = sqrt((anode.x - final.x)**2+(anode.y-final.y)**2)
                    if anode.openList == 1 :
                        if anode.c + anode.d > anode.h:  
                            continue
                    elif anode.openList == 0 :
                        anode.h = anode.c + anode.d 
                        anode.openList =1
                        lowestF.put((anode.h,next(unique),anode))                            
                    neighbor.append(anode)
                    
        

        
        
        
        
        for anode in neighbor:
            #anode.h = anode.c + anode.d    
            anode.openList = 1

            #keep track of ancestors
            anode.previous = current



# for live visualisation
        if live :
            for anode in grid:
                if anode.isWall ==1 :
                    pygame.draw.rect(display, (0,0,0), (anode.x*rectHeight,anode.y*rectWidth,rectWidth,rectHeight), 0)
                if anode.openList == 2:
                    pygame.draw.rect(display, (255,0,0), (anode.x*rectHeight,anode.y*rectWidth,rectWidth,rectHeight), 0)
                elif anode.openList == 1:
                    pygame.draw.rect(display, (0,255,0), (anode.x*rectHeight,anode.y*rectWidth,rectWidth,rectHeight), 0)
            
            #final node
            pygame.draw.rect(display, (0,255,0), (final.x*rectHeight,final.y*rectWidth,rectWidth,rectHeight), 0)
            
            for i in range(WIDTH):
                for j in range(HEIGHT):
                    pygame.draw.rect(display, (0,0,0), (i*rectHeight,j*rectWidth,rectWidth,rectHeight), THICKNESS)
        
            pygame.display.flip()
        




    for anode in grid:
        if anode.isWall ==1 :
            pygame.draw.rect(display, (0,0,0), (anode.x*rectHeight,anode.y*rectWidth,rectWidth,rectHeight), 0)
        if anode.openList == 2:
            pygame.draw.rect(display, (255,0,0), (anode.x*rectHeight,anode.y*rectWidth,rectWidth,rectHeight), 0)
        elif anode.openList == 1:
            pygame.draw.rect(display, (0,255,0), (anode.x*rectHeight,anode.y*rectWidth,rectWidth,rectHeight), 0)
    

    pygame.draw.rect(display, (0,255,0), (final.x*rectHeight,final.y*rectWidth,rectWidth,rectHeight), 0)
    
    for i in range(WIDTH):
        for j in range(HEIGHT):
            pygame.draw.rect(display, (0,0,0), (i*rectHeight,j*rectWidth,rectWidth,rectHeight), THICKNESS)

    
    # reconstruct path
    node = current;
    while (node.previous != None) :
        pygame.draw.rect(display, (0,0,255), (node.x*rectHeight,node.y*rectWidth,rectWidth,rectHeight), 0)
        node = node.previous
      
    pygame.display.flip()
    
    # input let you visualyze final path befor exit
    input()
    
    
    pass