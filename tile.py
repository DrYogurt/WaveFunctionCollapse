#!/usr/bin/env python
# coding: utf-8

class Tile:
    def __init__(self, name, board_prob, neighbor_probs, color):
        self.name = name
        self.b = board_prob
        self.n = neighbor_probs
        self.color = color

    
