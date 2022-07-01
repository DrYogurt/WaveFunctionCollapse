#!/usr/bin/env python
# coding: utf-8

class Tile:
    def __init__(self, name, edges) :
        self.name = name
        self.edges = edges #up right down left
        self.up = []
        self.right = []
        self.down = []
        self.left = []
    
    def make_adjacencies(self, tiles):
        for tile in tiles:
            if(self.edges[0] == tile.edges[2]):
                self.up.append(tile.name)
            if(self.edges[1] == tile.edges[3]):
                self.right.append(tile.name)
            if(self.edges[2] == tile.edges[0]):
                self.down.append(tile.name)
            if(self.edges[3] == tile.edges[1]):
                self.left.append(tile.name)
    
    @staticmethod
    def decode_tile(json_tile: dict):
        tile = Tile(json_tile["name"],json_tile["edges"])
        tile.up = json_tile["up"]
        tile.right = json_tile["right"]
        tile.down = json_tile["down"]
        tile.left = json_tile["left"]
        return tile
    
    @staticmethod
    def decode_json(json_txt):
        tiles = []
        for tile_dict in json.loads(json_txt):
            tiles.append(Tile.decode_tile(tile_dict))
        return tiles
 class Tile:
    def __init__(self, name, edges) :
        self.name = name
        self.edges = edges #up right down left
        self.up = []
        self.right = []
        self.down = []
        self.left = []
    
    def make_adjacencies(self, tiles):
        for tile in tiles:
            if(self.edges[0] == tile.edges[2]):
                self.up.append(tile.name)
            if(self.edges[1] == tile.edges[3]):
                self.right.append(tile.name)
            if(self.edges[2] == tile.edges[0]):
                self.down.append(tile.name)
            if(self.edges[3] == tile.edges[1]):
                self.left.append(tile.name)
    
    @staticmethod
    def decode_tile(json_tile: dict):
        tile = Tile(json_tile["name"],json_tile["edges"])
        tile.up = json_tile["up"]
        tile.right = json_tile["right"]
        tile.down = json_tile["down"]
        tile.left = json_tile["left"]
        return tile
    
    @staticmethod
    def decode_json(json_txt):
        tiles = []
        for tile_dict in json.loads(json_txt):
            tiles.append(Tile.decode_tile(tile_dict))
        return tiles
 class Tile:
    def __init__(self, name, edges) :
        self.name = name
        self.edges = edges #up right down left
        self.up = []
        self.right = []
        self.down = []
        self.left = []
    
    def make_adjacencies(self, tiles):
        for tile in tiles:
            if(self.edges[0] == tile.edges[2]):
                self.up.append(tile.name)
            if(self.edges[1] == tile.edges[3]):
                self.right.append(tile.name)
            if(self.edges[2] == tile.edges[0]):
                self.down.append(tile.name)
            if(self.edges[3] == tile.edges[1]):
                self.left.append(tile.name)
    
    @staticmethod
    def decode_tile(json_tile: dict):
        tile = Tile(json_tile["name"],json_tile["edges"])
        tile.up = json_tile["up"]
        tile.right = json_tile["right"]
        tile.down = json_tile["down"]
        tile.left = json_tile["left"]
        return tile
    
    @staticmethod
    def decode_json(json_txt):
        tiles = []
        for tile_dict in json.loads(json_txt):
            tiles.append(Tile.decode_tile(tile_dict))
        return tiles
 
