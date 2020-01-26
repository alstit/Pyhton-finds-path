'''
Created on 26 janv. 2020

@author: User
'''


import pygame
from math import sqrt
from random import random, randint


 

WIDTH = 100
HEIGHT = 100

SCREENWIDTH = 1000
SCREENHEIGHT = 1000


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
    
    def __init__(self,i,j):
        self.x = i
        self.y = j
        self.c = 1000
        self.d = 1000
        self.h  = self.c + self.d
        self.isWall = 0
        

if __name__ == '__main__':
    

    
    grid = []
    
    for i in range(HEIGHT):
        for j in range(WIDTH):
            grid.append(node(i,j))
    
    
    rectWidth = SCREENWIDTH / WIDTH
    rectHeight = SCREENHEIGHT / HEIGHT
    
    final = grid[80]
    
    x = None
    y = None

    
    pygame.init()
    display = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
    display.fill((255,255,255))
    
    FLAG_inputOK = 0
    for i in range(WIDTH-15):
        grid[int(HEIGHT/2)+i*(WIDTH)+WIDTH].isWall =1


        


    for i in range(WIDTH*HEIGHT - int((WIDTH*HEIGHT)/2)):
        grid[randint(0,len(grid)-1)].isWall = 1
    
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
                
        for i in range(WIDTH):
            for j in range(HEIGHT):
                pygame.draw.rect(display, (0,0,0), (i*rectHeight,j*rectWidth,rectWidth,rectHeight), 2)
                
        pygame.display.flip()
               
                
    
    for anode in grid :
        if anode.openList == 1:
            current = anode 
    current.d = sqrt((current.x - final.x)**2+(current.y-final.y)**2)
    current.h = current.c + current.d


    




    


    
    while(True):
        
            #pygame.time.wait(50)
        if current.x == final.x and current.y == final.y :
            print("WON")
            break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
        lowestF = []
        for anode in grid:
            if anode.openList == 1:
                lowestF.append(anode)
              
        current = lowestF[0]    
        for anode in lowestF : 
            if anode.h < current.h:
                current = anode
        
        for anode in grid:
            if anode.isWall == 1:
                continue
            if anode.x == current.x and anode.y == current.y:
                anode.openList = 2
        #for each neighbor of current
        

        
        
        
        neighbor = []
        for anode in grid:
            if anode.isWall:
                continue
            if anode.openList!=2:
                if anode.x == current.x + 1 and (anode.y == current.y or anode.y == current.y + 1 or anode.y == current.y - 1):
                    anode.c = current.c + 1
                    anode.d = sqrt((anode.x - final.x)**2+(anode.y-final.y)**2)
                    if anode.openList == 1 :
                        if anode.c + anode.d > anode.h:
                            continue 
                    neighbor.append(anode)
                    
                if anode.x == current.x - 1 and (anode.y == current.y or anode.y == current.y + 1 or anode.y == current.y - 1):
                    anode.c = current.c + 1
                    anode.d = sqrt((anode.x - final.x)**2+(anode.y-final.y)**2)
                    if anode.openList == 1 :
                        if anode.c + anode.d > anode.h:
                            continue
                    neighbor.append(anode)
                if anode.x == current.x and (anode.y == current.y + 1 or anode.y == current.y - 1):
                    anode.c = current.c + 1
                    anode.d = sqrt((anode.x - final.x)**2+(anode.y-final.y)**2)
                    if anode.openList == 1 :
                        if anode.c + anode.d > anode.h:  
                            continue                  
                    neighbor.append(anode)
                    
        
        for anode in neighbor:
            anode.h = anode.c + anode.d    
            anode.openList = 1
            anode.previous = current

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
                pygame.draw.rect(display, (0,0,0), (i*rectHeight,j*rectWidth,rectWidth,rectHeight), 2)
        
        
        
        
        pygame.display.flip()
        

    
    node = current;
    while (node.previous != None) :
        pygame.draw.rect(display, (0,0,255), (node.x*rectHeight,node.y*rectWidth,rectWidth,rectHeight), 0)
        node = node.previous
        
    pygame.display.flip()
    input()
    
    
    pass