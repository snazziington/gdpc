import math
from random import randint, choice
from gdpc import Editor, Block #, Transform
from gdpc.geometry import placeCuboid, placeCuboidHollow, placeRectOutline, placeCuboidWireframe

editor = Editor(buffering=True)

buildArea = editor.getBuildArea()

placeRectOutline(editor, buildArea.toRect(), 67, Block("red_concrete"))

# region HOUSE PLACEMENT
# Load world slice of the build area
editor.loadWorldSlice(cache=True)

# Get heightmap
heightmap = editor.worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"] # type: ignore

#  y = house floor height
y = heightmap[1, 1] # + 3 is temporary while i do blueprints

# x & z coordinates to build the house
houseX1 = buildArea.offset.x + 1
houseZ1 = buildArea.offset.z + 1

houseHeight = 7 #randint(5, 7)

# clear area
placeCuboid(editor, (houseX1, y, houseZ1), (houseX1 + 100, y + 20, houseZ1 + 100), Block("air"))
# endregion

# region HOUSE PALETTE
houseWalls = choice([
    Block ("mud_bricks"),
    Block ("brown_mushroom_block"),
    Block ("terracotta"),
    Block ("white_terracotta"),
    Block ("smooth_quartz"),
    Block ("smooth_sandstone"),
]) 

windowBlock = choice([
    Block("glass_pane"),
    Block("white_stained_glass_pane"),
    Block("brown_stained_glass_pane")
])

# endregion

# region LIVINGROOM
# Coordinates
# Width
lRoomWidth = 8 # choice([7, 9])
lRoomX1 = houseX1 + 25 # always n blocks from edge
lRoomX2 = lRoomX1 + lRoomWidth

#Depth
lRoomDepth = 14 # randint(13, 16)
lRoomZ1 = houseZ1 + 15 # always n blocks from edge
lRoomZ2 = lRoomZ1 + lRoomDepth

# Livingroom Palette
livingRoomFloor = Block("white_wool")

# Livingroom Wall
placeCuboidHollow(editor, (lRoomX1, y, lRoomZ1), (lRoomX2, y + houseHeight, lRoomZ2), houseWalls)

# Livingroom Floor
placeCuboidHollow(editor, (lRoomX1, y, lRoomZ1), (lRoomX2, y, lRoomZ2), livingRoomFloor)

# Livingroom Windows

windowPlacement = 2 #randint(1, 2)
print(windowPlacement)

windowY1 = y + windowPlacement
windowY2 = y + houseHeight - 2

# Front
placeCuboidHollow(editor, (lRoomX1 + 5, windowY1, lRoomZ1), (lRoomX2, windowY2, lRoomZ1), windowBlock)

# Side
placeCuboidHollow(editor, (lRoomX2, windowY1, lRoomZ1), (lRoomX2, windowY2, int((lRoomZ1 * .7 + lRoomZ2 * 0.3)) - 2), windowBlock)

# Back
placeCuboidHollow(editor, (lRoomX1, windowY1, lRoomZ2), (lRoomX2 - 1, windowY2, lRoomZ2), windowBlock)
# endregion

# region PORCH
# Coordinates
# Width
porchX1 = lRoomX1
porchX2 = lRoomX2

#Depth
porchDepth = 5
porchZ2 = lRoomZ1
porchZ1 = porchZ2 - porchDepth

# porch Palette
porchFloor = Block("pink_wool")

# porch is placed after the porch Roof
# endregion

# region GARAGE
# Coordinates
# Width
garageWidth = choice([7, 9])
garageDoorWidth = math.floor((garageWidth - 2) / 2)
garageX1 = lRoomX2 + 1
garageX2 = garageX1 + garageWidth
garageDoorsOpen = randint(0, 1)

# Depth
garageZ1 = int((lRoomZ1 * .7 + lRoomZ2 * 0.3))
garageZ2 = lRoomZ2

#Garage Palette
garageWall = Block("gray_concrete")
garageFloor = Block("gray_wool")
garageDoor = Block("pale_oak_door", {"facing": "east", "hinge": "right"})

# Garage Wall + Door
placeCuboidHollow(editor, (garageX1, y, garageZ1), (garageX2, y + houseHeight, garageZ2), garageWall)
editor.placeBlock((garageX1, y+1, garageZ2 - 2), garageDoor)
placeCuboidHollow(editor, (garageX1 - 1, y+1, garageZ2 - 2), (garageX1 - 1, y + 2, garageZ2 - 2), Block("air"))
garageLeftX1 = garageX2 - 1
garageRightX1 = garageX1 + 1

if garageDoorsOpen == 0:
    garageBigDoors = Block("iron_trapdoor", {"facing": "south", "half": "bottom", "open": "true"})
    garageLeftX2 = garageLeftX1 - garageDoorWidth
    garageRightX2 = garageRightX1 + garageDoorWidth

    # Left Big Door
    placeCuboidHollow(editor, (garageLeftX1, y + 1, garageZ1),
                    (garageLeftX2, y +  houseHeight - 1, garageZ1), garageBigDoors)

    # Right Big Door
    placeCuboidHollow(editor, (garageRightX1, y + 1, garageZ1),
                    (garageRightX2, y +  houseHeight - 1, garageZ1), garageBigDoors)

else:
    garageLeftDoors = Block("iron_trapdoor", {"facing": "west", "half": "bottom", "open": "true"})
    garageRightDoors = Block("iron_trapdoor", {"facing": "east", "half": "bottom", "open": "true"})
    garageLeftZ2 = garageZ1 - garageDoorWidth - 1
    garageLeftZ1 = garageZ1
    
    garageRightZ2 = garageZ1 - garageDoorWidth - 1
    garageRightZ1 = garageZ1

    # Left Big Door
    placeCuboidHollow(editor, (garageLeftX1, y + 1, garageLeftZ1),
                    (garageLeftX1, y +  houseHeight - 1, garageLeftZ2), garageLeftDoors)

    # Right Big Door
    placeCuboidHollow(editor, (garageRightX1, y + 1, garageRightZ1),
                    (garageRightX1, y +  houseHeight - 1, garageRightZ2), garageRightDoors)
    
    # Clear the space between the open doors
    placeCuboidHollow(editor, (garageLeftX1, y + 1, garageZ1),
                    (garageRightX1, y +  houseHeight - 1, garageZ1), Block("air"))
    
# Garage Floor
placeCuboidHollow(editor, (garageX1, y, garageZ1), (garageX2, y, garageZ2), garageFloor)
# endregion

# region HALLWAY
# Coordinates
# Width --- Should be dependent on the size of the rooms!
# Or actually; the rooms should be dependent on the size of the hallways.
hallwayWidth  = 3
hallwayLength = randint(10, 18) # randint(10, 20) # till 18---
hallwayX1 = lRoomX1
hallwayX2 = hallwayX1 - hallwayLength # randint(6, 8)

#Depth
hallwayZ1 = int((lRoomZ1 + lRoomZ2) / 2 - 2)
hallwayZ2 = hallwayZ1 + 3

# Hallway Palette
hallwayWall = Block("blue_concrete")
hallwayFloor = Block("blue_wool")

# Hallway Wall 
placeCuboidHollow(editor, (hallwayX1, y, hallwayZ1), (hallwayX2, y + houseHeight, hallwayZ2), houseWalls)

# Hallway Floor
placeCuboidHollow(editor, (hallwayX1, y, hallwayZ1), (hallwayX2, y, hallwayZ2), hallwayFloor) 

# Opens up hallway
placeCuboid(editor, (hallwayX1, y + 1, hallwayZ1), (hallwayX1, y +  houseHeight - 1, hallwayZ2), Block("air")) 

# Windows
placeCuboidHollow(editor, (hallwayX2, windowY1, hallwayZ1), (hallwayX2, windowY2, hallwayZ2), windowBlock)

# endregion

# region BEDROOMS

# region Bedroom #1   
bedroom1Width = math.floor(hallwayLength / 2)

# Coordinates
# Width
bedroom1X1 = lRoomX1 - bedroom1Width
bedroom1X2 = lRoomX1

# Depth
bedroom1Z1 = lRoomZ1
bedroom1Z2 = hallwayZ1

#Palette
bedroom1Wall = Block("red_concrete")
bedroom1Floor = Block("red_wool")

placeCuboidHollow(editor, (bedroom1X1, y, bedroom1Z1), (bedroom1X2, y + houseHeight, bedroom1Z2), houseWalls) 
placeCuboidHollow(editor, (bedroom1X1, y, bedroom1Z1), (bedroom1X2, y, bedroom1Z2), bedroom1Floor) 

# Windows
placeCuboidHollow(editor, (bedroom1X1, windowY1, bedroom1Z1), (bedroom1X2 - 1, windowY2, bedroom1Z1), windowBlock)
# endregion

# region Bedroom #2
bedroom2Width = math.ceil(hallwayLength / 2)

# Coordinates
# Width
bedroom2X1 = bedroom1X1 - bedroom2Width
bedroom2X2 = bedroom1X1

# Depth
bedroom2Z1 = lRoomZ1
bedroom2Z2 = hallwayZ1

#Palette
bedroom2Wall = Block("orange_concrete")
bedroom2Floor = Block("orange_wool")

placeCuboidHollow(editor, (bedroom2X1, y, bedroom2Z1), (bedroom2X2, y + houseHeight, bedroom2Z2), houseWalls) 
placeCuboidHollow(editor, (bedroom2X1, y, bedroom2Z1), (bedroom2X2, y, bedroom2Z2), bedroom2Floor) 
# endregion

if hallwayLength < 15:
    # Create a third bedroom next to the bathroom
    bedroomCount = 2
    kitchenWidth = math.floor(hallwayLength / 2) + 1
    bathroomWidth = hallwayLength - kitchenWidth
    
else:
    bedroomCount = 3
    kitchenWidth = math.floor(hallwayLength / 3)
    bathroomWidth = math.floor((hallwayLength - kitchenWidth) / 2)
    
    # region Bedroom #3
    bedroom3Width = hallwayLength - kitchenWidth - bathroomWidth

    # Coordinates
    # Width
    bedroom3X1 = lRoomX1 - kitchenWidth - bathroomWidth - bedroom3Width
    bedroom3X2 = lRoomX1 - kitchenWidth - bathroomWidth

    # Depth
    bedroom3Z1 = hallwayZ2
    bedroom3Z2 = lRoomZ2

    #Palette
    bedroom3Wall = Block("cyan_concrete")
    bedroom3Floor = Block("cyan_wool")

    placeCuboidHollow(editor, (bedroom3X1, y, bedroom3Z1), (bedroom3X2, y + houseHeight, bedroom3Z2), houseWalls) 
    placeCuboidHollow(editor, (bedroom3X1, y, bedroom3Z1), (bedroom3X2, y, bedroom3Z2), bedroom3Floor) 
    # endregion

# endregion

# region KITCHEN
# Coordinates
# Width
kitchenX1 = lRoomX1 - kitchenWidth
kitchenX2 = lRoomX1

# Depth
kitchenZ1 = lRoomZ2
kitchenZ2 = hallwayZ2

#Palette
kitchenWall = Block("yellow_concrete")
kitchenFloor = Block("yellow_wool")

placeCuboidHollow(editor, (kitchenX1, y, kitchenZ1), (kitchenX2, y + houseHeight, kitchenZ2), houseWalls) 
placeCuboidHollow(editor, (kitchenX1, y, kitchenZ1), (kitchenX2, y, kitchenZ2), kitchenFloor) 
# endregion

# region BATHROOM
# Coordinates
# Width
bathroomX1 = kitchenX1 - bathroomWidth
bathroomX2 = kitchenX1

# Depth
bathroomZ1 = lRoomZ2
bathroomZ2 = hallwayZ2

#Palette
bathroomWall = Block("green_concrete")
bathroomFloor = Block("green_wool")

placeCuboidHollow(editor, (bathroomX1, y, bathroomZ1), (bathroomX2, y + houseHeight, bathroomZ2), houseWalls) 
placeCuboidHollow(editor, (bathroomX1, y, bathroomZ1), (bathroomX2, y, bathroomZ2), bathroomFloor) 

# endregion

# region FOUNDATION
houseX2 = lRoomX2
houseZ2 = lRoomZ2
foundationBlock = Block("cobblestone")
placeCuboidWireframe(editor, (bedroom2X1, y, lRoomZ1), (houseX2, y, houseZ2), foundationBlock)
# endregion

# region ROOF
roofX1 = porchX1 + int(lRoomWidth / 2)
roofZ1 = porchZ1 + 4

roofBlock = choice([
    #"dark_oak",
    #"red_nether_brick",
    #"mangrove",
    #"spruce",
    #"polished_granite",
    #"nether_brick",
    "polished_blackstone_brick",
])

northRoofBlock = Block(roofBlock + "_stairs", {"facing": "north"})
eastRoofBlock = Block(roofBlock + "_stairs", {"facing": "east"})
southRoofBlock = Block(roofBlock + "_stairs", {"facing": "south"})
westRoofBlock = Block(roofBlock + "_stairs", {"facing": "west"})
topRoofBlock = Block(roofBlock + "_slab")

# region House Roof
houseRoofX1 = bedroom2X1 - 1
houseRoofZ1 = lRoomZ1 - 1

houseRoofX2 = lRoomX2 + 1
houseRoofZ2 = lRoomZ2 + 1
houseRoofHeight = math.ceil(lRoomDepth / 2) + 1

for i in range(0, houseRoofHeight):
    yy = y +  houseHeight + i
    #placeCuboidWireframe(editor, (houseRoofX1 + i, yy, houseRoofZ1 + i), (houseRoofX2 - i, yy, houseRoofZ2 - i), Block("glass"))
    placeCuboidWireframe(editor, (houseRoofX1 + i, yy, houseRoofZ1 + i), (houseRoofX1 + i, yy, houseRoofZ2 - i), eastRoofBlock) # right
    placeCuboidWireframe(editor, (houseRoofX2 - i, yy, houseRoofZ1 + i), (houseRoofX2 - i, yy, houseRoofZ2 - i), westRoofBlock) # left
    
    placeCuboidWireframe(editor, (houseRoofX1 + i, yy, houseRoofZ1 + i), (houseRoofX2 - i, yy, houseRoofZ1 + i), southRoofBlock) # front
    placeCuboidWireframe(editor, (houseRoofX1 + i, yy, houseRoofZ2 - i), (houseRoofX2 - i, yy, houseRoofZ2 - i), northRoofBlock) # back

houseWidth = lRoomX2 - bedroom2X1 + 1
houseRoofWidth = houseWidth + 2 # + 2 due to overhang

# Adds a slab to the top of the roof if there is an opening
if lRoomDepth % 2 == 0:
    houseRoofTopLength = (houseRoofWidth - (houseRoofHeight * 2)) - 1
    
    placeCuboid(editor, (houseRoofX1 + houseRoofHeight, y +  houseHeight + houseRoofHeight, houseRoofZ1 + houseRoofHeight),
                (houseRoofX1 + houseRoofTopLength + houseRoofHeight, y +  houseHeight + houseRoofHeight, houseRoofZ1 + houseRoofHeight),
                Block(roofBlock + "_slab"))
    
# endregion

# region Porch Roof
porchRoofX1 = porchX1 - 1
porchRoofZ1 = porchZ1 - 1

porchRoofX2 = porchX2 + 1
porchRoofZ2 = porchZ2 + 10

porchRoofHeight = math.floor(lRoomWidth / 2) + 1
for i in range(0, porchRoofHeight):
    yy = y +  houseHeight + i
    #placeCuboidWireframe(editor, (porchRoofX1 + i, yy, porchRoofZ1 + i), (porchRoofX2 - i, yy, porchRoofZ2 - i), Block("glass"))
    placeCuboidWireframe(editor, (porchRoofX1 + i, yy, porchRoofZ1 + i), (porchRoofX1 + i, yy, porchRoofZ1 + i + porchRoofHeight), eastRoofBlock) # right
    placeCuboidWireframe(editor, (porchRoofX2 - i, yy, porchRoofZ1 + i), (porchRoofX2 - i, yy, porchRoofZ2 - i), westRoofBlock) # left
    
    placeCuboidWireframe(editor, (porchRoofX1 + i, yy, porchRoofZ1 + i), (porchRoofX2 - i, yy, porchRoofZ1 + i), southRoofBlock) # front
    #placeCuboidWireframe(editor, (porchRoofX1 + i, yy, porchRoofZ2 - i), (porchRoofX2 - i, yy, porchRoofZ2 - i), northRoofBlock) # back

if porchRoofHeight % 2 == 1:
    placeCuboid(editor, (porchRoofX1 + porchRoofHeight, y +  houseHeight + porchRoofHeight, porchRoofZ1 + porchRoofHeight),
                (porchRoofX1 + porchRoofHeight, y +  houseHeight + porchRoofHeight, porchRoofZ1 + porchRoofHeight * 2 - 1),
                Block(roofBlock + "_slab"))

# endregion

# PORCH PLACEMENT
# porch Wall
placeCuboidWireframe(editor, (porchX1, y, porchZ1), (porchX2, y + houseHeight, porchZ2), houseWalls)

# porch Ceiling
placeCuboidHollow(editor, (porchX1, y + houseHeight, porchZ1), (porchX2, y + houseHeight, porchZ2), porchFloor)

# porch Floor
placeCuboidHollow(editor, (porchX1, y, porchZ1), (porchX2, y, porchZ2), porchFloor)

# endregion
# Removes top layer so I can see blueprint
#placeCuboid(editor, (houseX1, y + houseHeight, houseZ1), (houseX1 + 100, y +  houseHeight + 1 , houseZ1 + 100), Block("air"))


# Add double doors
editor.placeBlock((lRoomX1+2, y+1, lRoomZ1), Block("oak_door", {"facing": "south", "hinge": "right"}))
editor.placeBlock((lRoomX1+3, y+1, lRoomZ1), Block("oak_door", {"facing": "south", "hinge": "left"}))