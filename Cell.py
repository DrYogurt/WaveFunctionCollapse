#!/usr/bin/env python
# coding: utf-8

class Cell:
    def __init__(self, *options):
        self.options = list(options)
        self.collapsed = False
        self.state = None
    
    def collapse(self):
        self.state = random.choice(self.options)
        self.collapsed = True
        self.options = [self.state]
    
    def update(self):
        if len(self.options) == 1:
            self.collapse()
 
