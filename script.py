#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import json, curses, random, time
from cell import Cell
from tile import Tile
from graph import Graph

def from_adjacency_json(filename):
    with open(filename) as f:
        all_data = json.load(f)
        tiles = {}
        cell_data = all_data["cell_data"]
        names = list(cell_data)
        adjacencies = all_data["adjacencies"]    
        
        for i in range(len(names)):
            name = names[i]
            b = cell_data[name]["b"]
            color = cell_data[name]["color"]
            nbrs = {}
            for j in range(len(names)):
                nbrs[names[j]] = adjacencies[i][j]
            tiles[names[i]] = Tile(name,b,nbrs,color)
        return tiles

def update_curses(screen, graph, dim):
    for row in range(dim):
        for col in range(dim):
            c = graph.grid[row*dim + col]
            c_draw = ""
            if c.state is None:
                c_draw = "*"
            else:
                c_draw = c.state[0]
            screen.addch(row,col,c_draw)
    screen.addstr(dim+1,0,"Average Entropy: {}".format(graph.calc_entropy()))
    screen.refresh()
    return

def to_ent(graph,dim):
    im = []
    for row in range(dim):
        im.append([])
        for col in range(dim):
            im[row].append(graph.grid[row*dim+col].entropy)
    return im

def to_img(graph,dim):
    im = []
    for row in range(dim):
        im.append([])
        for col in range(dim):
            c = graph.grid[row*dim + col]
            im[row].append(tiles[c.state].color)
    return im

def draw_progress(screen,progress,length):
    bar_str = "["
    done = round(progress*length)
    for i in range(done):
        bar_str = bar_str + "="
    if done < length:
        bar_str = bar_str + ">"
        for i in range(length - done - 1):
            bar_str = bar_str + " "
    bar_str = bar_str + "]"
    screen.addstr(0,0,bar_str)
    screen.addstr(1,0,"Percent Complete: {}".format(round(progress,4)))
    screen.refresh()

if __name__ == "__main__":
    
    dim = 30
    starting_tiles = 10
    
    tiles = from_adjacency_json("nine_test.json")

    show_entropy = False #keep as false, adding in options for cool stuff later
    show_updates = True

    screen = curses.initscr()

    
    if show_entropy:
        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111)
    
    graph = Graph(dim,dim,tiles,do_scale=1)
    done = False

    for _ in range(starting_tiles):
        graph.collapse_next(c_idx=random.randint(0,dim*dim))
    
    while not done:
        while not graph.q.empty():
            #time.sleep(.01)
            graph.update_board()
                
            if show_entropy:
                ax.imshow(to_ent(graph,dim))
                fig.canvas.draw()
                fig.canvas.flush_events()
            
            if show_updates:
                update_curses(screen,graph,dim)
            else:
                draw_progress(screen,1.0 - graph.calc_entropy(),round(dim / 2))
        
        c = graph.collapse_next()
        done = c is None
    plt.imshow(to_img(graph,dim))
    plt.show()
    #curses.endwin()
