#!/usr/bin/env python
# coding: utf-8

import numpy as np
import math

class Cell:
    def __init__(self, options):
        self.options = options
        self.collapsed = False
        self.state = None
        self.entropy = 1
        self.calculate_entropy()
    
    def collapse(self,state=None):
        if state is not None:
            self.state = state
        else:
            self.state = np.random.choice([state for state,prob in self.options.items()], p=[prob for state,prob in self.options.items()])
        for state,prob in self.options.items():
            self.options[state] = 1 if state == self.state else 0
        self.collapsed = True
        self.entropy = 0.0
        
    
    def update(self):
        if self.collapsed:
            return
        self.calculate_entropy()
        if self.entropy < 0.22:
            self.collapse()
            return
        else:
            return
 
    def calculate_entropy(self):
        ent = 0.0
        for state, prob in self.options.items():
            ent = ent + (0 if prob == 0.0 else prob*math.log(prob, len(self.options)))
        self.entropy = -1.0 * ent
