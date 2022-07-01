#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import json, curses, random, time
from queue import Queue
        


def update_curses(screen, graph, names, dim):
    for row in range(dim):
        for col in range(dim):
            c = graph[row*dim + col]
            c_draw = str(len(c.options)) if c.state is None else c.state[0]
            screen.addch(row,col,c_draw)
    screen.refresh()
                
def draw(tiles,dim,screen,num_init=1):
    names = [tile.name for tile in tiles] # initialize cell options
    graph = gen_graph(dim,dim,names) # initialize graph    
    # the plan is to create a queue,starting with collapsed cells
    # and visiting their neighbors, eventually
    q = Queue()
    for i in range(num_init):
        currInit = random.randint(0,len(graph)-1)
        graph[currInit].collapse()
        q.put(currInit)
    update_curses(screen, graph, names, dim)
    
    while(True): #TODO insert condition here
        while not q.empty():
            update_curses(screen, graph, names, dim)
            time.sleep(0.005)
            c_idx = q.get()
            #print(c_idx)
            c = graph[c_idx]
            # look up
            if(c_idx >= dim):
                nbr = graph[c_idx - dim] #define the neighbor
                if(not nbr.collapsed):
                    new_op = [o for o in nbr.options if o in valid_neighbors(c,tiles,"up")]
                    if(set(new_op) != set(nbr.options)):
                        q.put(c_idx - dim)
                        nbr.options = new_op
                        nbr.update()
            # look right
            if(c_idx % dim < dim - 1):
                nbr = graph[c_idx + 1]
                if(not nbr.collapsed):
                    new_op = [o for o in nbr.options if o in valid_neighbors(c,tiles,"right")]
                    if(set(new_op) != set(nbr.options)):
                        q.put(c_idx + 1)
                        nbr.options = new_op
                        nbr.update()

            # look down
            if(c_idx / dim < dim - 1):
                nbr = graph[c_idx + dim]
                if(not nbr.collapsed):
                    new_op = [o for o in nbr.options if o in valid_neighbors(c,tiles,"down")]
                    if(set(new_op) != set(nbr.options)):
                        q.put(c_idx + dim)
                        nbr.options = new_op
                        nbr.update()

            # look left
            if(c_idx % dim != 0):
                nbr = graph[c_idx - 1]
                if(not nbr.collapsed):
                    new_op = [o for o in nbr.options if o in valid_neighbors(c,tiles,"left")]
                    if(set(new_op) != set(nbr.options)):
                        q.put(c_idx - 1)
                        nbr.options = new_op
                        nbr.update()
        
        ordered = list(filter(lambda x: not x[1].collapsed,enumerate(graph))) # pull out all the non-collapsed cells
        if(len(ordered) == 0): #check if we're done
            update_curses(screen, graph, names, dim)
            return graph
        ordered.sort(key=lambda c: len(c[1].options))
        q.put(ordered[0][0])
        ordered[0][1].collapse()

def to_img(graph,dim):
    im = []
    colors = {
            "FOREST":[8,91,33],
            "GRASS":[14,181,64],
            "BEACH":[221,199,124],
            "WATER":[95,155,239]
            }
    for row in range(dim):
        im.append([])
        for col in range(dim):
            c = graph[row*dim + col]
            im[row].append(colors[c.state])
    return im


wo_adj = '[ { "name": "FOREST", "edges": [ "A", "A", "A", "A" ], "up": [ "FOREST", "GRASS" ], "right": [ "FOREST", "GRASS" ], "down": [ "FOREST", "GRASS" ], "left": [ "FOREST", "GRASS" ] }, { "name": "GRASS", "edges": [ "A", "A", "A", "A" ], "up": [ "FOREST", "GRASS", "BEACH" ], "right": [ "FOREST", "GRASS", "BEACH" ], "down": [ "FOREST", "GRASS", "BEACH" ], "left": [ "FOREST", "GRASS", "BEACH" ] }, { "name": "BEACH", "edges": [ "A", "A", "A", "A" ], "up": [ "GRASS", "BEACH", "WATER" ], "right": [ "GRASS", "BEACH", "WATER" ], "down": [ "FOREST", "GRASS", "BEACH", "WATER" ], "left": [ "GRASS", "BEACH", "WATER" ] }, { "name": "WATER", "edges": [ "A", "A", "A", "A" ], "up": [ "BEACH", "WATER" ], "right": [ "BEACH", "WATER" ], "down": [ "BEACH", "WATER" ], "left": [ "BEACH", "WATER" ] }]'

if __name__ == "__main__":
    dim = 25
    tiles = Tile.decode_json(wo_adj)
    screen = curses.initscr()
    graph = draw(tiles,dim,screen)
    plt.imshow(to_img(graph,dim))
    plt.show()
    curses.endwin()



"""

tiles = []
tiles.append(Tile("FOREST",("A","A","A","A")))
tiles.append(Tile("GRASS",("A","A","A","A")))
tiles.append(Tile("BEACH",("A","A","A","A")))
tiles.append(Tile("WATER",("A","A","A","A")))
for tile in tiles:
    tile.make_adjacencies(tiles)
json.dumps([tile.__dict__ for tile in tiles])
"""
