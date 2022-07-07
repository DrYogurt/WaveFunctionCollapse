#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import json, curses, random, time
from cell import Cell
from tile import Tile
from graph import Graph


def update_curses(screen, graph, names, dim):
    for row in range(dim):
        for col in range(dim):
            c = graph.grid[row*dim + col]
            c_draw = ""
            if c.state is None:
                c_draw = "*"
            else:
                c_draw = c.state[0]
            screen.addch(row,col,c_draw)
    screen.refresh()

def to_ent(graph,dim):
    im = []
    for row in range(dim):
        im.append([])
        for col in range(dim):
            im[row].append(graph.grid[row*dim+col].entropy)
    return im

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
            c = graph.grid[row*dim + col]
            im[row].append(colors[c.state])
    return im
third = 1.0 / 3.0
forest = Tile("FOREST",0.25,{"FOREST":0.55,
    "GRASS":0.35,
    "BEACH":0.0,
    "WATER":0.1})
grass = Tile("GRASS",0.25,{"FOREST":0.30,
    "GRASS":0.35,
    "BEACH":0.35,
    "WATER":0.0})
beach = Tile("BEACH",0.25,{"FOREST":0.0,
    "GRASS":0.34,
    "BEACH":0.31,
    "WATER":0.33})
water = Tile("WATER",0.25,{"FOREST":0.05,
    "GRASS":0.0,
    "BEACH":0.45,
    "WATER":0.5})

tiles = {
    "FOREST":forest,
    "GRASS":grass,
    "BEACH":beach,
    "WATER":water
}

def run_in_background(row,col,graph=None,starting_tiles=0):
    if graph is None:
        graph = Graph(dim,dim,tiles)
    for _ in range(starting_tiles):
        graph.collapse_next(c_idx=random.randint(0,row*col))
    done = False
    while not done:
        counter = 0
        while not graph.q.empty():   
            graph.update_board()
        c = graph.collapse_next()
        done = c is None
    return graph

if __name__ == "__main__":
    
    dim = 25
    disp = False 
    if not disp:
        dim = 100
        g = run_in_background(dim,dim,starting_tiles=5)
        plt.imshow(to_img(g,dim))
        plt.show()
    
    screen = curses.initscr()
    """
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    """
    graph = Graph(dim,dim,tiles)
    done = False
    
    graph.collapse_next(c_idx=random.randint(dim,dim*3),c_state="FOREST")
    graph.collapse_next(c_idx=random.randint(dim*7,dim*dim),c_state="WATER")

    while not done:
        counter = 0
        while not graph.q.empty(): # and counter < dim*dim*dim:  
            graph.update_board()
            
            update_curses(screen,graph,graph.names,dim)
            #screen.addstr(dim+1,dim,str(len(list(graph.q.queue))))
            #ax.imshow(to_ent(graph,dim))
            #fig.canvas.draw()
            #fig.canvas.flush_events()
            counter = counter + 1
        #print(counter)
        c = graph.collapse_next()
        done = c is None
    plt.imshow(to_img(graph,dim))
    plt.show()
    #curses.endwin()



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
