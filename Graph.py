#!/usr/bin/env_python
# coding: utf-8
class Graph:
    def __init__(self,row,col,tiles):
        self.grid = [] #using a 1d graph for easier sorting (by least entropy)
        self.row = row
        self.col = col
        self.tiles = tiles
        self.names = [tile.name for tile in tiles] # initialize cell options
        self.gen_grid()
        self.q = Queue()


def gen_grid(self):
    for j in range(0,row*col):
        self.grid.append(Cell(*names))
    return

#TODO: decide if this is the best way to select neighbors
def valid_neighbors(cell, tiles):
    vld_ngbrs = set()
    for name in cell.options:        
        for t in tiles:
            if name == t.name:
                tile = t
        for ngbr in tile.__dict__[direction]:
            vld_ngbrs.add(ngbr)
    return vld_ngbrs
