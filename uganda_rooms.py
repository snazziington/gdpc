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
y = heightmap[1, 1] + 3# + 3 is temporary while i do blueprints

# region VARIABLE PCG
# House Sizing
houseHeight = randint(5, 7) # determines height of house
print("houseHeight: ", houseHeight)

lRoomDepth = randint(13, 16) # livingRoom depth
print("lRoomDepth: ", lRoomDepth)

lRoomWidth = randint(7, 9) # livingRoom width
print("lRoomWidth: ", lRoomWidth)

hallwayLength = randint(10, 18) # length of hallway. if > 15, third bedroom spawns
print("hallwayLength: ", hallwayLength)

# Toggleables
garageHouse = randint(0,1) # 1 = garage spawns, 0 = no garage
garageDoorsOpen = 0 # defaults to 0 if garage does not exist
print("garageHouse: ", garageHouse)
if garageHouse == 1:
    garageDoorsOpen = randint(0, 1) # 0 = garage doors shut, 1 = garade doors open
    print("garageDoorsOpen: ", garageDoorsOpen)

# x & z coordinates to build the house
houseX1 = buildArea.offset.x + 1 + 20 # temp + 20
houseZ1 = buildArea.offset.z + 1 + 20 # temp + 20

# clear area
placeCuboid(editor, (houseX1 - 25, y - 2, houseZ1 - 25), (houseX1 + 60, y + 20, houseZ1 + 50), Block("air"))

# House Sizing
houseBoundingX1 = houseX1 - hallwayLength
houseBoundingX2 = houseX1 + lRoomWidth
houseBoundingZ1 = houseZ1
houseBoundingZ2 = houseZ1 + lRoomDepth

# House
placeCuboidWireframe(editor, (houseBoundingX1, y, houseBoundingZ1),
                    (houseBoundingX2, y + 15, houseBoundingZ2), Block("red_wool"))

# Garage Sizing
garageWidth = choice([7, 9])
print("garageWidth: ", garageWidth)
garageDoorWidth = math.floor((garageWidth - 2) / 2)

# House's outer bounds
# Porch
porchBoundingX1 = houseX1
porchBoundingX2 = houseX1 + lRoomWidth
porchBoundingZ1 = houseBoundingZ1 - 5
porchBoundingZ2 = houseBoundingZ1
placeCuboidWireframe(editor, (porchBoundingX1, y, porchBoundingZ1), # porch depth is always 5
                    (porchBoundingX2, y + 10, porchBoundingZ2), Block("green_wool"))

# Garage (if present)
garageBoundingX1 = porchBoundingX2 + 1
garageBoundingX2 = garageBoundingX1 + garageWidth
garageBoundingZ1 = int(houseZ1 * .7 + (houseZ1 + lRoomDepth) * 0.3)
garageBoundingZ2 = houseBoundingZ2
if garageHouse == 1 and garageDoorsOpen == 0:
    placeCuboidWireframe(editor, (garageBoundingX1, y, garageBoundingZ1), # porch depth is always 5
                    (garageBoundingX2, y + 10, garageBoundingZ2), Block("blue_wool"))
elif garageDoorsOpen == 1 and garageDoorsOpen == 1:
    placeCuboidWireframe(editor, (garageBoundingX1, y, garageBoundingZ1 - 4), # porch depth is always 5
                    (garageBoundingX2, y + 10, garageBoundingZ2), Block("blue_wool"))

# endregion

# region Block Palettes
houseWalls = choice([
    Block ("mud_bricks"),
    Block ("brown_mushroom_block"),
    Block ("terracotta"),
    Block ("white_terracotta"),
    Block ("smooth_quartz"),
    Block ("smooth_sandstone"),
    Block ("yellow_terracotta"),
]) 

windowBlock = choice([
    Block("glass_pane"),
    Block("white_stained_glass_pane"),
    Block("brown_stained_glass_pane")
])

porchFloor = choice([
    Block("gray_terracotta"),
    Block("light_gray_terracotta"),
    Block("brown_terracotta"),
])

foundationBlock = choice([
    Block("cobblestone"),
    Block("bricks"),
    Block("cobblestone")
])

roofBlock = choice([
    "dark_oak",
    "red_nether_brick",
    "mangrove",
    "spruce",
    "nether_brick",
    "polished_blackstone_brick",
])

porchFenceBlock = choice([
    Block("dark_oak_fence"),
    Block("oak_fence"),
    Block("spruce_fence"),
    Block("jungle_fence"),
    Block("nether_brick_fence"),
    Block("crimson_fence"),
])

porchWall = choice([
    Block("dark_oak_planks"),
])

# endregion

# region LIVINGROOM

# Coordinates
# Width
lRoomX1 = houseX1 # always n blocks from edge
lRoomX2 = lRoomX1 + lRoomWidth

#Depth
lRoomZ1 = houseZ1 # always n blocks from edge
lRoomZ2 = lRoomZ1 + lRoomDepth

# Livingroom Palette
livingRoomFloor = Block("white_wool")

# Livingroom Wall
placeCuboidHollow(editor, (lRoomX1, y, lRoomZ1), (lRoomX2, y + houseHeight, lRoomZ2), houseWalls)

# Livingroom Floor
placeCuboidHollow(editor, (lRoomX1, y, lRoomZ1), (lRoomX2, y, lRoomZ2), livingRoomFloor)

# Livingroom Windows

wallPlacement = 2

windowY1 = y + wallPlacement
windowY2 = y + houseHeight - 2

# Front
placeCuboidHollow(editor, (lRoomX1 + 5, windowY1, lRoomZ1), (lRoomX2, windowY2, lRoomZ1), windowBlock)

if houseHeight > 5:
    placeCuboidHollow(editor, (lRoomX1+2, y+4, lRoomZ1), (lRoomX1+3, y+4, lRoomZ1), windowBlock)

# Side
if garageHouse == 1:
    placeCuboidHollow(editor, (lRoomX2, windowY1, lRoomZ1), (lRoomX2, windowY2, int((lRoomZ1 * .7 + lRoomZ2 * 0.3)) - 2), windowBlock)
else:
    placeCuboidHollow(editor, (lRoomX2, windowY1, lRoomZ1), (lRoomX2, windowY2, lRoomZ2 - 1), windowBlock)
    livingroomWindowWidth = lRoomZ2 - lRoomZ1 - 1
    if livingroomWindowWidth == 15:
        windowSeparator1 = lRoomZ1 + 4
        windowSeparator2 = lRoomZ1 + 8
        windowSeparator3 = lRoomZ1 + 12
        placeCuboid(editor, (lRoomX2, windowY1, windowSeparator1), (lRoomX2, windowY2, windowSeparator1), houseWalls)
        placeCuboid(editor, (lRoomX2, windowY1, windowSeparator2), (lRoomX2, windowY2, windowSeparator2), houseWalls)
        placeCuboid(editor, (lRoomX2, windowY1, windowSeparator3), (lRoomX2, windowY2, windowSeparator3), houseWalls)
    elif livingroomWindowWidth == 12:
        windowSeparator1 = lRoomZ1 + 4
        windowSeparator2 = lRoomZ1 + 9
        placeCuboid(editor, (lRoomX2, windowY1, windowSeparator1), (lRoomX2, windowY2, windowSeparator1), houseWalls)
        placeCuboid(editor, (lRoomX2, windowY1, windowSeparator2), (lRoomX2, windowY2, windowSeparator2), houseWalls)
    elif livingroomWindowWidth == 14:
        windowSeparator1 = lRoomZ1 + 5
        windowSeparator2 = lRoomZ1 + 10
        placeCuboid(editor, (lRoomX2, windowY1, windowSeparator1), (lRoomX2, windowY2, windowSeparator1), houseWalls)
        placeCuboid(editor, (lRoomX2, windowY1, windowSeparator2), (lRoomX2, windowY2, windowSeparator2), houseWalls)
    elif livingroomWindowWidth == 13:
        windowSeparator1 = lRoomZ1 + 3
        windowSeparator2 = lRoomZ1 + 6
        windowSeparator3 = lRoomZ1 + 8
        windowSeparator4 = lRoomZ1 + 11
        placeCuboid(editor, (lRoomX2, windowY1, windowSeparator1), (lRoomX2, windowY2, windowSeparator1), houseWalls)
        placeCuboid(editor, (lRoomX2, windowY1, windowSeparator2), (lRoomX2, windowY2, windowSeparator2), houseWalls)
        placeCuboid(editor, (lRoomX2, windowY1, windowSeparator3), (lRoomX2, windowY2, windowSeparator3), houseWalls)
        placeCuboid(editor, (lRoomX2, windowY1, windowSeparator4), (lRoomX2, windowY2, windowSeparator4), houseWalls)
# Back
placeCuboidHollow(editor, (lRoomX1, windowY1, lRoomZ2), (lRoomX2 - 1, windowY2, lRoomZ2), windowBlock)

livingRoomBackWidth = lRoomX2 - lRoomX1 - 1

if livingRoomBackWidth == 7:
    wallPlacement = int((lRoomX2 + lRoomX1) / 2)
    placeCuboid(editor, (wallPlacement, windowY1, lRoomZ2), (wallPlacement, windowY2, lRoomZ2), houseWalls)
elif livingRoomBackWidth == 8:
    wallPlacement1 = lRoomX1 + 3
    wallPlacement2 = lRoomX1 + 6
    placeCuboid(editor, (wallPlacement1, windowY1, lRoomZ2), (wallPlacement1, windowY2, lRoomZ2), houseWalls)
    placeCuboid(editor, (wallPlacement2, windowY1, lRoomZ2), (wallPlacement2, windowY2, lRoomZ2), houseWalls)
# endregion

# region PORCH
# Porch is placed after the porch roof
# Coordinates
# Width
porchX1 = lRoomX1
porchX2 = lRoomX2

#Depth
porchDepth = 5
porchZ2 = lRoomZ1
porchZ1 = porchZ2 - porchDepth

# region GARAGE
# Coordinates
# Width

garageX1 = lRoomX2 + 1
garageX2 = garageX1 + garageWidth


# Depth
garageZ1 = int((lRoomZ1 * .7 + lRoomZ2 * 0.3))
garageZ2 = lRoomZ2

#Garage Palette
garageWall = Block("gray_concrete")
garageFloor = Block("gray_wool")
garageDoor = Block("pale_oak_door", {"facing": "east", "hinge": "right"})

# Garage Wall + Door
if garageHouse == 1:
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
hallwayX1 = lRoomX1
hallwayX2 = hallwayX1 - hallwayLength

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

if any([hallwayLength == 12, hallwayLength == 13, hallwayLength == 16, hallwayLength == 17]):
    wallPlacement = int((bedroom1X1 + bedroom1X2) / 2)
    placeCuboid(editor, (wallPlacement, windowY2, bedroom1Z1), (wallPlacement, windowY2, bedroom1Z1), houseWalls)

elif hallwayLength == 14 or hallwayLength == 15:
    wallPlacement1 = bedroom1X1 + 2
    wallPlacement2 = bedroom1X1 + 5
    placeCuboid(editor, (wallPlacement1, windowY2, bedroom1Z1), (wallPlacement1, windowY2, bedroom1Z1), houseWalls)
    placeCuboid(editor, (wallPlacement2, windowY2, bedroom1Z1), (wallPlacement2, windowY2, bedroom1Z1), houseWalls)

elif hallwayLength == 18:
    wallPlacement1 = bedroom1X1 + 3
    wallPlacement2 = bedroom1X1 + 6
    placeCuboid(editor, (wallPlacement1, windowY1, bedroom1Z1), (wallPlacement1, windowY2, bedroom1Z1), houseWalls)
    placeCuboid(editor, (wallPlacement2, windowY1, bedroom1Z1), (wallPlacement2, windowY2, bedroom1Z1), houseWalls)
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

# Windows
placeCuboidHollow(editor, (bedroom2X1 + 1, windowY1, bedroom2Z1), (bedroom2X2 - 1, windowY2, bedroom2Z1), windowBlock) # front
placeCuboidHollow(editor, (bedroom2X1, windowY1, bedroom2Z1 + 1), (bedroom2X1, windowY2, bedroom2Z2 - 1), windowBlock) # side
if any([hallwayLength == 12, hallwayLength == 15, hallwayLength == 16]):
    wallPlacement = int((bedroom2X1 + bedroom2X2) / 2)
    placeCuboid(editor, (wallPlacement, windowY2, bedroom2Z1), (wallPlacement, windowY2, bedroom2Z1), houseWalls)
elif hallwayLength == 13 or hallwayLength == 14:
    wallPlacement1 = bedroom2X1 + 2
    wallPlacement2 = bedroom2X1 + 5
    placeCuboid(editor, (wallPlacement1, windowY2, bedroom2Z1), (wallPlacement1, windowY2, bedroom2Z1), houseWalls)
    placeCuboid(editor, (wallPlacement2, windowY2, bedroom2Z1), (wallPlacement2, windowY2, bedroom2Z1), houseWalls)

elif hallwayLength == 17:
    wallPlacement1 = bedroom2X1 + 3
    wallPlacement2 = bedroom2X1 + 6
    placeCuboid(editor, (wallPlacement1, windowY2, bedroom2Z1), (wallPlacement1, windowY2, bedroom2Z1), houseWalls)
    placeCuboid(editor, (wallPlacement2, windowY2, bedroom2Z1), (wallPlacement2, windowY2, bedroom2Z1), houseWalls)

elif hallwayLength == 18:
    wallPlacement1 = bedroom2X1 + 3
    wallPlacement2 = bedroom2X1 + 6
    placeCuboid(editor, (wallPlacement1, windowY1, bedroom2Z1), (wallPlacement1, windowY2, bedroom2Z1), houseWalls)
    placeCuboid(editor, (wallPlacement2, windowY1, bedroom2Z1), (wallPlacement2, windowY2, bedroom2Z1), houseWalls)
# endregion

if hallwayLength < 15:
    bedroomCount = 2
    kitchenWidth = math.floor(hallwayLength / 2) + 1
    bathroomWidth = hallwayLength - kitchenWidth
    
else:
    # If hallway longer than 15, create a third bedroom next to the bathroom
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

    # Windows
    # Back
    placeCuboidHollow(editor, (bedroom3X1 + 1, windowY1, bedroom3Z2), (bedroom2X2 - 1, windowY2, bedroom3Z2), windowBlock)
    bedroom3WindowWidth = bedroom3Width - 1
    if bedroom3WindowWidth == 5:
        wallPlacement = int((bedroom3X2 + bedroom3X1) / 2)
        placeCuboid(editor, (wallPlacement, windowY1, bedroom3Z2), (wallPlacement, windowY2, bedroom3Z2), houseWalls)
    
    # Side
    placeCuboidHollow(editor, (bedroom3X1, windowY1, bedroom3Z1 + 1), (bedroom2X1, windowY2, bedroom3Z2 - 1), windowBlock)

    if lRoomDepth == 14 or lRoomDepth == 15:
        wallPlacement = int((bedroom3Z2 + bedroom3Z1) / 2)
        placeCuboid(editor, (bedroom3X1, windowY1, wallPlacement), (bedroom3X1, windowY2, wallPlacement), houseWalls)
    elif lRoomDepth == 16:
        wallPlacement1 = bedroom3Z1 + 2
        wallPlacement2 = bedroom3Z1 + 5
        placeCuboid(editor, (bedroom3X1, windowY1, wallPlacement1), (bedroom3X1, windowY2, wallPlacement1), houseWalls)
        placeCuboid(editor, (bedroom3X1, windowY1, wallPlacement2), (bedroom3X1, windowY2, wallPlacement2), houseWalls)
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

#Windows
placeCuboidHollow(editor, (kitchenX1 + 1, y + 2, kitchenZ1), (kitchenX2 - 1, windowY2, kitchenZ1), windowBlock)
kitchenWidth = kitchenX2 - kitchenX1 - 1
print("kitchenWidth: ", kitchenWidth)
if kitchenWidth % 2 == 1:
    wallPlacement = int((kitchenX2 + kitchenX1) / 2)
    placeCuboid(editor, (wallPlacement, windowY1, lRoomZ2), (wallPlacement, windowY2, lRoomZ2), houseWalls)
elif kitchenWidth == 6:
    wallPlacement1 = kitchenX1 + 2
    wallPlacement2 = kitchenX1 + 5
    placeCuboid(editor, (wallPlacement1, windowY1, lRoomZ2), (wallPlacement1, windowY2, lRoomZ2), houseWalls)
    placeCuboid(editor, (wallPlacement2, windowY1, lRoomZ2), (wallPlacement2, windowY2, lRoomZ2), houseWalls)

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

#Windows
placeCuboidHollow(editor, (bathroomX1 + 1, windowY2, bathroomZ1), (bathroomX2 - 1, windowY2, bathroomZ1), windowBlock)

# Places window at end of house if there is no 3rd bedroom
if hallwayLength < 15:
    placeCuboidHollow(editor, (bathroomX1, windowY2, bathroomZ2 + 1), (bathroomX1, windowY2, bathroomZ1 - 1), windowBlock)

bathroomWidth = bathroomX2 - bathroomX1 - 1
print("bathroomWidth: ", bathroomWidth)
if bathroomWidth == 5:
    wallPlacement = int((bathroomX2 + bathroomX1) / 2)
    placeCuboidHollow(editor, (wallPlacement, windowY2, bathroomZ1), (wallPlacement, windowY2, bathroomZ1), houseWalls)
# endregion

# region FOUNDATION
houseX2 = lRoomX2
houseZ2 = lRoomZ2
placeCuboidHollow(editor, (bedroom2X1, y - 2, lRoomZ1), (houseX2, y - 1, houseZ2), foundationBlock)
placeCuboidWireframe(editor, (bedroom2X1, y - 2, lRoomZ1), (houseX2, y, houseZ2), foundationBlock)
# endregion

# region ROOF
roofX1 = porchX1 + int(lRoomWidth / 2)
roofZ1 = porchZ1 + 4

northRoofBlock = Block(roofBlock + "_stairs", {"facing": "north"})
eastRoofBlock = Block(roofBlock + "_stairs", {"facing": "east"})
southRoofBlock = Block(roofBlock + "_stairs", {"facing": "south"})
westRoofBlock = Block(roofBlock + "_stairs", {"facing": "west"})
topRoofBlock = Block(roofBlock + "_slab")

# region House Roof
houseRoofX1 = bedroom2X1 - 2
houseRoofZ1 = lRoomZ1 - 2

houseRoofX2 = lRoomX2 + 2
houseRoofZ2 = lRoomZ2 + 2
houseRoofHeight = math.ceil(lRoomDepth / 2) + 2

for i in range(0, houseRoofHeight):
    yy = y +  houseHeight + i
    #placeCuboidWireframe(editor, (houseRoofX1 + i, yy, houseRoofZ1 + i), (houseRoofX2 - i, yy, houseRoofZ2 - i), Block("glass"))
    placeCuboidWireframe(editor, (houseRoofX1 + i, yy, houseRoofZ1 + i), (houseRoofX1 + i, yy, houseRoofZ2 - i), eastRoofBlock) # right
    placeCuboidWireframe(editor, (houseRoofX2 - i, yy, houseRoofZ1 + i), (houseRoofX2 - i, yy, houseRoofZ2 - i), westRoofBlock) # left
    
    placeCuboidWireframe(editor, (houseRoofX1 + i, yy, houseRoofZ1 + i), (houseRoofX2 - i, yy, houseRoofZ1 + i), southRoofBlock) # front
    placeCuboidWireframe(editor, (houseRoofX1 + i, yy, houseRoofZ2 - i), (houseRoofX2 - i, yy, houseRoofZ2 - i), northRoofBlock) # back

houseWidth = lRoomX2 - bedroom2X1 + 1
houseRoofWidth = houseWidth + 2 # + 2 due to overhang

# Clear excess of roof
placeCuboidWireframe(editor, (lRoomX1 + 1, y + houseHeight, houseRoofZ1), (lRoomX2 - 1, y + houseHeight, houseRoofZ1), Block("air")) # back
editor.placeBlock((lRoomX2 + 1, y + houseHeight, lRoomZ1 - 2), Block("air"))
# Adds a slab to the top of the roof if there is an opening
if lRoomDepth % 2 == 0:
    houseRoofTopLength = (houseRoofWidth - (houseRoofHeight * 2)) + 1
    
    placeCuboid(editor, (houseRoofX1 + houseRoofHeight, y +  houseHeight + houseRoofHeight, houseRoofZ1 + houseRoofHeight),
                (houseRoofX1 + houseRoofTopLength + houseRoofHeight, y +  houseHeight + houseRoofHeight, houseRoofZ1 + houseRoofHeight),
                Block(roofBlock + "_slab"))
    
# endregion

# region Porch Roof
porchRoofX1 = porchX1 - 2
porchRoofZ1 = porchZ1 - 2

porchRoofX2 = porchX2 + 2
porchRoofZ2 = porchZ2 + 10

porchRoofHeight = math.floor(lRoomWidth / 2) + 3
for i in range(0, porchRoofHeight):
    yy = y +  houseHeight + i
    #placeCuboidWireframe(editor, (porchRoofX1 + i, yy, porchRoofZ1 + i), (porchRoofX2 - i, yy, porchRoofZ2 - i), Block("glass"))
    placeCuboidWireframe(editor, (porchRoofX1 + i, yy, porchRoofZ1 + i), (porchRoofX1 + i, yy, porchRoofZ1 + i + porchRoofHeight - 2), eastRoofBlock) # right
    placeCuboidWireframe(editor, (porchRoofX2 - i, yy, porchRoofZ1 + i), (porchRoofX2 - i, yy, porchRoofZ2 - i), westRoofBlock) # left
    
    placeCuboidWireframe(editor, (porchRoofX1 + i, yy, porchRoofZ1 + i), (porchRoofX2 - i, yy, porchRoofZ1 + i), southRoofBlock) # front
    #placeCuboidWireframe(editor, (porchRoofX1 + i, yy, porchRoofZ2 - i), (porchRoofX2 - i, yy, porchRoofZ2 - i), northRoofBlock) # back

porchWidth = porchRoofX2 - porchRoofX1 + 1
print("porchWidth:", porchWidth)
if porchWidth % 2 == 1:
    placeCuboid(editor, (porchRoofX1 + porchRoofHeight - 1, y +  houseHeight + porchRoofHeight - 1, porchRoofZ1 + porchRoofHeight - 1),
                (porchRoofX1 + porchRoofHeight - 1, y +  houseHeight + porchRoofHeight - 1, porchRoofZ1 + porchRoofHeight * 2 - 4),
                Block(roofBlock + "_slab"))

# endregion

# region PORCH PLACEMENT

# porch fences
placeCuboid(editor, (porchX1, y + 1, porchZ1),
                  (porchX2, y + 1, porchZ1), porchFenceBlock)
placeCuboid(editor, (porchX2, y + 1, porchZ1),
                  (porchX2, y + 1, porchZ2), porchFenceBlock)
placeCuboid(editor, (porchX1, y + 1, porchZ1),
                  (porchX1, y + 1, porchZ2), porchFenceBlock)

# Opens up area for stairs
placeCuboidWireframe(editor, (porchX1, y + 1, porchZ1 + 2),
                  (porchX1, y + 1, porchZ2 - 2), Block("air"))


# porch Wall
placeCuboidWireframe(editor, (porchX1, y, porchZ1), (porchX2, y + houseHeight, porchZ2), porchWall)
placeCuboidWireframe(editor, (porchX1, y, porchZ2), (porchX2, y + houseHeight, porchZ2), houseWalls)

# porch Ceiling
porchCeiling = y + houseHeight + 1
placeCuboidHollow(editor, (porchX1 + 1, porchCeiling, porchZ1 + 1),
                  (porchX2 - 1, porchCeiling, porchZ2 - 1), porchFloor)

# porch Ceiling decor
porchCeilingDecor = choice([
    Block("dark_oak_slab", {"type": "top"}),
    Block("spruce_slab", {"type": "top"}),
    Block("mud_brick_slab", {"type": "top"}),
])
placeCuboidWireframe(editor, (porchX1 + 1, porchCeiling - 1, porchZ1 + 1),
                  (porchX2 - 1, porchCeiling - 1, porchZ2 - 1), porchCeilingDecor)

# porch Floor
placeCuboidHollow(editor, (porchX1, y, porchZ1), (porchX2, y, porchZ2), porchFloor)

# endregion
# endregion
# Removes top layer so I can see blueprint
#placeCuboid(editor, (houseX1, y + houseHeight, houseZ1), (houseX1 + 100, y +  houseHeight + 1 , houseZ1 + 100), Block("air"))


# Add double doors
editor.placeBlock((lRoomX1+2, y+1, lRoomZ1), Block("oak_door", {"facing": "south", "hinge": "right"}))
editor.placeBlock((lRoomX1+3, y+1, lRoomZ1), Block("oak_door", {"facing": "south", "hinge": "left"}))