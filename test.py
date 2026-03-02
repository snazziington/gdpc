from random import randint, choice
from gdpc import Editor, Block
from gdpc.geometry import placeCuboid, placeCuboidHollow

editor = Editor(buffering=True)

buildArea = editor.getBuildArea()

# Finding floor
# Load world slice of the build area
editor.loadWorldSlice(cache=True)

# Get heightmap
heightmap = editor.worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

y = heightmap[5,5]

x = buildArea.offset.x + 1
z = buildArea.offset.z + 1

height = randint(15, 30)
depth  = randint(15, 30)

# Random floor palette
floorPalette = [
    Block("mossy_cobblestone"),
    Block("obsidian"),
    Block("red_wool"),
    Block("sponge"),
]

# Choose wall material
wallBlock = choice([
    Block("spruce_planks"),
    Block("white_terracotta"),
    Block("green_terracotta"),
])
print(f"Chosen wall block: {wallBlock}")

# Build main shape
placeCuboidHollow(editor, (x, y, z), (x+depth, y+height, z+depth), floorPalette)
placeCuboid(editor, (x, y, z), (x+depth, y, z+depth), Block("water"))

# Build roof: loop through distance from the middle
# range(a, b) = number of roof rows - 1
for dx in range(1, 4):
    # height of roof rows
    yy = y + height + 2 - dx

    # Build row of stairs blocks
    leftBlock  = Block("oak_stairs", {"facing": "east"})
    rightBlock = Block("oak_stairs", {"facing": "west"})
    placeCuboid(editor, (x+2-dx, yy, z-1), (x+2-dx, yy, z+depth+1), leftBlock)
    placeCuboid(editor, (x+2+dx, yy, z-1), (x+2+dx, yy, z+depth+1), rightBlock)

# build the top row of the roof
yy = y + height + 1
placeCuboid(editor, (x+2, yy, z-1), (x+2, yy, z+depth+1), Block("oak_planks"))

# Add a door
doorBlock = Block("oak_door", {"facing": "south", "hinge": "left"})
editor.placeBlock((x+2, y+1, z), doorBlock)