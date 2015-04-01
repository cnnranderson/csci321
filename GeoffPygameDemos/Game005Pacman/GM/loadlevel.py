import resource
import object

def loadroomtiles(roomfile, roomdict, tilefile, config, obj):
    """Populates a room with non-animated objecst with images
       from a strip file.
       roomdict should be a char:int dictionary translating the
       characters in the room into subimages from the tile strip
       file"""
    f = open(roomfile, 'r')
    rowstrings = f.read().split('\n')
    tiles = resource.get_strip(tilefile, config)
    width, height = tiles.images[0].get_size()
    y = height/2
    for row in rowstrings:
        x = width/2
        for letter in row:
            if roomdict.has_key(letter):
                i = roomdict[letter]
                strip = resource.Strip([tiles.images[i]], 1)
                obj((x,y),strip)
            x += width
        y += height

def loadroomobjects(roomfile, char, obj, spritesize):
    """Populates a room with objects, everywhere """
    f = open(roomfile, 'r')
    rowstrings = f.read().split('\n')
    width, height = spritesize
    y = height/2
    for row in rowstrings:
        x = width/2
        for letter in row:
            if letter == char:
                obj((x,y))
            x += width
        y += height
