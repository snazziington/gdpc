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

#  y = Foundation height
y = heightmap[15, 15] + 3 # + 3 is temporary while i do blueprints

garageLeft = 0 # randint(0, 1)

# x & z coordinates to build the house
houseX = buildArea.offset.x + 1
houseZ = buildArea.offset.z + 1

height = 3

# LIVINGROOM
# Coordinates
# Width
lRoomX1 = houseX + 10 # always 10 blocks from edge
lRoomX2 = lRoomX1 + 10

#Depth
lRoomZ1 = houseZ # + 10 # always 10 blocks from edge
lRoomZ2 = lRoomZ1 + randint(12, 16)

# Livingroom Palette
livingRoomWall = Block("white_concrete")
livingRoomFloor = Block("white_wool")

# Livingroom Wall
placeCuboidHollow(editor, (lRoomX1, y, lRoomZ1), (lRoomX2, y + height, lRoomZ2), livingRoomWall)

# Livingroom Floor
placeCuboidHollow(editor, (lRoomX1, y, lRoomZ1), (lRoomX2, y, lRoomZ2), livingRoomFloor)

# GARAGE
# Coordinates
# Width
if garageLeft == 1:
    garageX1 = lRoomX2
    garageX2 = garageX1 + randint(6, 8)
    print("Garage is left")

else:
    garageX1 = lRoomX1
    garageX2  = garageX1 - randint(6, 8)
    print("Garage is right")

# Depth
garageZ1 = int((lRoomZ1 * .7 + lRoomZ2 * 0.3))
garageZ2 = lRoomZ2

#Garage Palette
garageWall = Block("gray_concrete")
garageFloor = Block("gray_wool")

# Garage Wall + Door
placeCuboidHollow(editor, (garageX1, y, garageZ1), (garageX2, y + height, garageZ2), garageWall)
garageDoor = Block("pale_oak_door", {"facing": "west", "hinge": "left"})
editor.placeBlock((garageX1, y+1, garageZ2 - 2), garageDoor)

# Garage Floor
placeCuboidHollow(editor, (garageX1, y, garageZ1), (garageX2, y, garageZ2), garageFloor)

# region HALLWAY
# Coordinates
# Width --- Should be dependent on the size of the rooms!
# Or actually; the rooms should be dependent on the size of the hallways.
hallwayWidth  = 3
if garageLeft == 1:
    hallwayX1 = lRoomX1
    hallwayX2 = hallwayX1 - 10 # randint(6, 8)

else:
    hallwayX1 = lRoomX2
    hallwayX2 = hallwayX1 + 10 # randint(6, 8)

#Depth
hallwayZ1 = (lRoomZ1 + lRoomZ2) / 2
hallwayZ2 = hallwayZ1 + 3

# Hallway Palette
hallwayWall = Block("blue_concrete")
hallwayFloor = Block("blue_wool")

# Hallway Wall
placeCuboidHollow(editor, (hallwayX1, y, hallwayZ1), (hallwayX2, y + height, hallwayZ2), hallwayWall)

# Hallway Floor
placeCuboidHollow(editor, (hallwayX1, y, hallwayZ1), (hallwayX2, y, hallwayZ2), hallwayFloor)


# Removes top layer so I can see blueprint
placeCuboid(editor, (houseX, y + 3, houseZ), (houseX + 30, y + 3, houseZ + 30), Block("air"))

# Add double doors
editor.placeBlock((lRoomX1+2, y+1, lRoomZ1), Block("oak_door", {"facing": "south", "hinge": "right"}))
editor.placeBlock((lRoomX1+3, y+1, lRoomZ1), Block("oak_door", {"facing": "south", "hinge": "left"}))