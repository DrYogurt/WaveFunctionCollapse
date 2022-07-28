#!/usr/bin/env_python
# coding: utf-8

from cell import Cell
from queue import Queue

class Graph:
    def __init__(self,row,col,tiles,do_scale=0):
        self.grid = []
        self.tiles = tiles
        self.row = row
        self.col = col
        self.do_scale = do_scale
        self.names = list(tiles) # initialize cell options
        self.gen_graph()
        self.q = Queue()
    
    def grid2coords(self,idx):
        row = int(idx / self.col)
        col = int(idx % self.col)
        return row,col

    def coords2grid(self,row,col):
        return row * self.col + col

    def gen_graph(self):
        for _ in range(self.row*self.col):
            options = {}
            for name in self.names:
                options[name]=self.tiles[name].b
            self.grid.append(Cell(options))
    
    def calc_realprobs(self): 
        global_probs = {}
        for state in self.names:
            global_probs[state] = 0
            for cell in self.grid:
                global_probs[state] = global_probs[state] + cell.options[state]
            global_probs[state] = global_probs[state] / len(self.grid)
        return global_probs

    def calc_entropy(self):
        total_ent = 0
        for cell in self.grid:
            total_ent = total_ent + cell.entropy
        return total_ent / len(self.grid)

    def calc_PN(self,c_idx):
        thisr,thisc = self.grid2coords(c_idx)
        up = 1
        left = 1
        right = 1
        down = 1
        if thisr > 0:
            up = sum([self.tiles[state].b*prob for state,prob in self.grid[self.coords2grid(thisr-1,thisc)].options.items()])
        if thisr < self.row-1:
            down = sum([self.tiles[state].b*prob for state,prob in self.grid[self.coords2grid(thisr+1,thisc)].options.items()])
        if thisc > 0:
            left = sum([self.tiles[state].b*prob for state,prob in self.grid[self.coords2grid(thisr,thisc-1)].options.items()])
        if thisc < self.col-1:
            right = sum([self.tiles[state].b*prob for state,prob in self.grid[self.coords2grid(thisr,thisc+1)].options.items()])
        return up*right*down*left

    def calc_PNS(self,c_idx,c_state):
        thisr,thisc = self.grid2coords(c_idx)
        up = 1
        left = 1
        right = 1
        down = 1
        if thisr > 0:
            up = sum([self.tiles[state].n[c_state]*prob for state,prob in self.grid[self.coords2grid(thisr-1,thisc)].options.items()])
        if thisr < self.row-1:
            down = sum([self.tiles[state].n[c_state]*prob for state,prob in self.grid[self.coords2grid(thisr+1,thisc)].options.items()])
        if thisc > 0:
            left = sum([self.tiles[state].n[c_state]*prob for state,prob in self.grid[self.coords2grid(thisr,thisc-1)].options.items()])
        if thisc < self.col-1:
            right = sum([self.tiles[state].n[c_state]*prob for state,prob in self.grid[self.coords2grid(thisr,thisc+1)].options.items()])

        return up*right*down*left

    def update_state(self,c_idx):
        self.grid[c_idx].update()
        if self.grid[c_idx].collapsed:
            return True
        real_b = self.calc_realprobs()
        normalizer = 0
        new_opts = {}
        for state,prob in self.grid[c_idx].options.items():
            # P(S) is given as the prior probability of the cell
            pS = prob
            
            # P(N) is given as the probability of a specific neighbor state
            pN = self.calc_PN(c_idx)
            
            #P(N|S) is given as the probability of the neighbor state given a suppposed state
            pNS = self.calc_PNS(c_idx,state)

            pSN = pNS * pS / pN
            
            
            if self.do_scale == 1:
                pSN = 0 if real_b[state] == 0 else pSN * self.tiles[state].b / real_b[state] #scaling factor
            normalizer = normalizer + pSN
            new_opts[state] = pSN
        
        did_update = False
        if normalizer == 0:
            print("uhoh")
            self.grid[c_idx].collapse()
            return True
        for state,prob in self.grid[c_idx].options.items():
            new_opts[state] = new_opts[state] / normalizer
            did_update = did_update or (round(new_opts[state],3) != round(self.grid[c_idx].options[state],3))
            self.grid[c_idx].options[state] = new_opts[state]

        return did_update

    def update_board(self):
        counter = 0
        #while not self.q.empty():# and counter < self.row*self.col:
        c_idx = self.q.get()
        thisr,thisc = self.grid2coords(c_idx)
        did_update = self.update_state(c_idx)
        if did_update:
            if thisr > 0:
                cur_nbr = c_idx-self.row
                if(not self.grid[cur_nbr].collapsed and cur_nbr not in list(self.q.queue)):
                    self.q.put(cur_nbr)
            if thisr < self.row-1:
                cur_nbr = c_idx+self.row
                if(not self.grid[cur_nbr].collapsed and cur_nbr not in list(self.q.queue)):
                    self.q.put(cur_nbr)
            if thisc > 0:
                cur_nbr = c_idx - 1
                if(not self.grid[cur_nbr].collapsed and cur_nbr not in list(self.q.queue)):
                    self.q.put(cur_nbr)
            if thisc < self.col-1:
                cur_nbr = c_idx+1
                if(not self.grid[cur_nbr].collapsed and cur_nbr not in list(self.q.queue)):
                    self.q.put(cur_nbr)
        counter = counter + 1
        return counter
            
    def collapse_next(self,c_idx=None,c_state=None):
        if c_idx is not None:
            self.q.put(c_idx)
            self.grid[c_idx].collapse(c_state)
            return c_idx
        ordered = list(filter(lambda x: not x[1].collapsed,enumerate(self.grid))) # pull out all the non-collapsed cells
        if(len(ordered) == 0): #check if we're done
            return None
        ordered.sort(key=lambda c: c[1].entropy) # change to less entropy
        self.q.put(ordered[0][0])
        ordered[0][1].collapse()
        return(ordered[0][0])

    def __str__(self):
        gstr = ""
        for row in range(self.row):
            for col in range(self.col):
                c = self.grid(self.coords2grid(row,col))
                if c.collapsed:
                    gstr = gstr + c.state[0] + " "
                else:
                    gstr = gstr + "*" + " "
            gstr = gstr + "\n"
        return gstr
