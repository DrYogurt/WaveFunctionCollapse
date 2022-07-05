#!/usr/bin/env python
# coding: utf-8

class Tile:
    def __init__(self, name, board_prob, neighbor_probs):
        self.name = name
        self.b = board_prob
        self.n = neighbor_probs


