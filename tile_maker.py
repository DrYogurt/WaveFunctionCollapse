from tile import Tile

num_tiles = input("how many tiles")

tile_names = []
for i in range(num_tiles):
    name = input("Enter tile {}".format(i))

tile_str = str(tile_names)

tile_nbrs = {}
for i in range(num_tiles):
    print(tile_str)
    nbrs = input("input nbrs for tile {}".format(tile_names[i]))
    tile_nbrs[tile_names[i]] = nbrs.split(" ")



