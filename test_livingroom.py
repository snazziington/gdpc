from random import randint, choice
from gdpc import Editor, Block
from gdpc.geometry import placeCuboid, placeCuboidHollow

editor = Editor(buffering=True)

buildArea = editor.getBuildArea()

# region Deciding Floor Level

# Load world slice of the build area
editor.loadWorldSlice(cache=True)

# Get heightmap
heightmap = editor.worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

# i guess y is equal to the average heighmap??????? idk man
y = heightmap[5,5]

# endregion




# region Deciding X/Z Coords
x = buildArea.offset.x + 1
z = buildArea.offset.z + 1

# endregion

# region Black Palette
# Floor
floorPalette = [
    Block("stone_bricks"),
    Block("cracked_stone_bricks"),
    Block("cobblestone"),
]

# Wall
wallBlock = choice([
    Block("white_terracotta"),
    Block("brown_terracotta"),
    Block("black_terracotta"),
])
print(f"Chosen wall block: {wallBlock}")

# endregion


# region Room Sizes
houseHeight  = randint(6, 15)
air = Block("air")

widthLRoom   = randint(3, 7) * 2 - 1 # odd number
depthLRoom   = randint(8, 15)

widthKitchen = randint(3, 7) * 2 - 1 # odd number
depthKitchen = randint(8, 15)
wallKitchen = Block("pink_terracotta")



# endregion


# i will eventually want to generate the livingroom away from the edges of the buildarea so i can have rooms either
# side of the livingroom.
# i will also want to make some potted plants in the front near the windows
# dear god i'm gonna have to make windows
# i will need to make if statements maybe. like if divisible by xyz and bigger than xyz then do this pattern of windows blah blah
# i will have to figure out a formula yippeeeeeeeeeeeeeeeee!!

# Build livingroom
placeCuboidHollow(editor, (x, y, z), (x + widthLRoom, y + houseHeight, z + depthLRoom), wallBlock)
placeCuboid(editor, (x, y, z), (x + widthLRoom, y, z + depthLRoom), floorPalette)

# maybe I could even redefine x and Z? or like. have a xLRoom and zLRoom variable fo rthe boundaries of the
# lroom? so the formulas aren't that long + wordy

# what i could also do is 1. generate a random number between 3 and 7. 2. create that number of rooms 3. each
# room is assignmened a different purpose (lroom/bedroom/kitchen/bathroom?), room 1 is always livingroom?
# and that could be how things are generated? so instead of widthKitchen itd be widthRoom1
# but then there's the issue of room sizes not making sense 9e.g., no one needs a bathroom the size of a like, 
# master bedroom lmao.


# Build kitchen
placeCuboidHollow(editor, (x + widthLRoom, y, z),
                          (x + widthKitchen + widthLRoom, y + houseHeight, z + depthKitchen),
                           wallKitchen)

# clear the space between the kitchen 
placeCuboid(editor, (x + widthLRoom, y, z),
                    (x + widthLRoom, y + houseHeight - 1, z + depthLRoom),
                     air)
placeCuboid(editor, (x, y, z + depthLRoom), (x+widthKitchen, y, z), Block("white_concrete"))

# Build roof: loop through distance from the middle
# range(a, b) = number of roof rows - 1
for dx in range(1, 4):
    # height of roof rows
    yy = y + houseHeight + 2 - dx

    # Build row of stairs blocks
    leftBlock  = Block("oak_stairs", {"facing": "east"})
    rightBlock = Block("oak_stairs", {"facing": "west"})
    placeCuboid(editor, (x+2-dx, yy, z-1), (x+2-dx, yy, z+depthLRoom+1), leftBlock)
    placeCuboid(editor, (x+2+dx, yy, z-1), (x+2+dx, yy, z+depthLRoom+1), rightBlock)

# build the top row of the roof
yy = y + houseHeight + 1
placeCuboid(editor, (x+2, yy, z-1), (x+2, yy, z+depthLRoom+1), Block("oak_planks"))

# Add a door
doorBlock = Block("oak_door", {"facing": "south", "hinge": "left"})
editor.placeBlock((x+2, y+1, z), doorBlock)