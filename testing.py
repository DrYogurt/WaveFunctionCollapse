import matplotlib.pyplot as plt
import json, curses, random, time
from cell import Cell
from tile import Tile
from graph import Graph

# define our tiles

forest = Tile("FOREST",0.25,{"FOREST":0.6,
    "GRASS":0.3,
    "BEACH":0.0,
    "WATER":0.1})
grass = Tile("GRASS",0.25,{"FOREST":0.3,
    "GRASS":0.4,
    "BEACH":0.2,
    "WATER":0.1})
beach = Tile("FOREST",0.25,{"FOREST":0.0,
    "GRASS":0.2,
    "BEACH":0.2,
    "WATER":0.6})
water = Tile("FOREST",0.25,{"FOREST":0.1,
    "GRASS":0.1,
    "BEACH":0.6,
    "WATER":0.2})
"""

forest = Tile("FOREST",0.25,{"FOREST":0.0,
    "GRASS":0.5,
    "BEACH":0.5,
    "WATER":0.0})
grass = Tile("GRASS",0.25,{"FOREST":0.5,
    "GRASS":0.0,
    "BEACH":0.5,
    "WATER":0.0})
beach = Tile("BEACH",0.25,{"FOREST":0.0,
    "GRASS":0.5,
    "BEACH":0.0,
    "WATER":0.5})
water = Tile("WATER",0.25,{"FOREST":0.0,
    "GRASS":0.5,
    "BEACH":0.5,
    "WATER":0.0})
"""


tiles = {
    "FOREST":forest,
    "GRASS":grass,
    "BEACH":beach,
    "WATER":water
}

def print_board():
    for row in range(dim):
        for col in range(dim):
            c = graph.grid[graph.coords2grid(row,col)]
            if c.collapsed:
                print(c.state[0],end="\t")
            else:
                print(c.entropy,end="\t")
        print()

dim = 5
graph = Graph(dim,dim,tiles)
#graph.collapse_next()
#graph.update_board()

print_board()
print("\n")
graph.grid[12].collapse()
graph.q.put(12)
print_board()
print("\n")
for _ in range(2):
    to_update = list(graph.q.queue)
    print(to_update)
    graph.update_board()
    print_board()
    print(graph.grid[to_update[0]].__dict__)
    print("\n")