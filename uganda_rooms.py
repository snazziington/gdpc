import math, statistics
from random import randint, choice
from gdpc import Editor, Block
from gdpc.geometry import placeCuboid, placeCuboidHollow, placeRectOutline, placeCuboidWireframe, placeCheckeredCuboid
from gdpc.interface import runCommand

editor = Editor(buffering=True)

buildArea = editor.getBuildArea()
placeRectOutline(editor, buildArea.toRect(), 100, Block("red_concrete"))

# region BUILD HOUSE LAYOUT
# region HOUSE PLACEMENT
# Load world slice of the build area
editor.loadWorldSlice(cache=True)

# Get heightmap
heightmap = editor.worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"] # type: ignore
waterHeightmap = editor.worldSlice.heightmaps["OCEAN_FLOOR"] # type: ignore

# x & z coordinates to build the house
buildAreaX1 = buildArea.offset.x + 1
buildAreaZ1 = buildArea.offset.z + 1

#  region FIND FLAT FLOOR
global heightMapList
heightMapList = []

global heightMapAverages
heightMapAverages = []

global flattestLandCoords
flattestLandCoords = []

lowestStdDev = 10

pillarHeight = 1

# region ROOM SIZE PCG
# House, Livingroom, Hallway Sizing
houseHeight = randint(5, 7) # determines height of house
print("houseHeight: ", houseHeight)

lRoomDepth = randint(13, 16) # livingRoom depth
print("lRoomDepth: ", lRoomDepth)

lRoomWidth = randint(7, 9) # livingRoom width
print("lRoomWidth: ", lRoomWidth)

hallwayLength = randint(12, 18) # length of hallway. if > 15, third bedroom spawns
print("hallwayLength: ", hallwayLength)

# Garage Sizing
garageWidth = choice([7, 9])
garageDepth = math.floor(lRoomDepth * .7)
print("garageWidth: ", garageWidth)
print("garageDepth: ", garageDepth)
garageDoorWidth = math.floor((garageWidth - 2) / 2)

# Garage Toggle
garageHouse = randint(0,1) # 1 = garage spawns, 0 = no garage
garageDoorsOpen = 1 # defaults to 0 if garage does not exist
print("garageHouse: ", garageHouse)
if garageHouse == 1:
    garageDoorsOpen = randint(0, 1) # 0 = garage doors shut, 1 = garage doors open
    print("garageDoorsOpen: ", garageDoorsOpen)
# endregion

# region HOUSE BOUNDS

# House Total Dimensions
if garageHouse == 1:
    houseTotalWidth = garageWidth + lRoomWidth + hallwayLength
else:
    houseTotalWidth = lRoomWidth + hallwayLength
houseTotalDepth = lRoomDepth + 5 # porchDepth is always 5

# Total
houseTotalWidth = garageWidth + lRoomWidth + hallwayLength
houseTotalDepth = lRoomDepth + 5

# For the entire build area
def calcHeightMap(x: int, z: int):
    heightMapList = []
    for xX in range (x, x + houseTotalWidth):
        for zZ in range (z, z + houseTotalDepth):
            y = heightmap[xX, zZ]
            y = int(y)
            heightMapList.append(y) # type: ignore

    global lowestStdDev
    global newStdDev

    newStdDev = float(statistics.stdev(heightMapList))
    if newStdDev < lowestStdDev:
            if notSubmergedInWater():
                lowestStdDev = newStdDev

                global averageY
                averageY = int(statistics.mean(heightMapList))
                global lowestX
                lowestX = x

                global lowestZ
                lowestZ = z

                global pillarHeight
                pillarHeight += 1
                y = int(heightmap[lowestX, lowestZ] + 2) + 20

def notSubmergedInWater():
    global waterCount
    waterCount = 0

    global nonWaterCount
    nonWaterCount = 0
    for xX in range (x, x + houseTotalWidth):
        if xX % 2 == 0:
            for zZ in range (z, z + houseTotalDepth):
                if zZ % 2 == 0:
                    y = waterHeightmap[xX, zZ]
                    y = int(y)
                    
                    for i in range (0, 3):
                        block = str(editor.getBlock((xX + buildArea.offset.x, y + i, zZ + buildArea.offset.z)))
                        if "water" in block:
                            waterCount += 1
                        else:
                            nonWaterCount += 1

    if nonWaterCount * 0.6 > waterCount:
       return True
    else:
        print("Too much water! Finding new build area")
        return False

for x in range (2, 100 - houseTotalWidth - 4):
    if x % 2 == 0:
        for z in range (2, 100 - houseTotalDepth - 4):
            if z % 2 == 0:
                calcHeightMap(x, z)
print("Lowest stdDev is found at: ", lowestX, lowestZ, "and is: ", lowestStdDev)

y1 = heightmap[lowestX, lowestZ] - 1
y2 = heightmap[lowestX + houseTotalWidth, lowestZ + houseTotalDepth] - 1

y = averageY + 1

buildAreaX1 = lowestX + buildArea.offset.x
buildAreaZ1 = lowestZ + buildArea.offset.z

# House Bounds
houseBoundingX1 = buildAreaX1 + 2
houseBoundingX2 = houseBoundingX1 + lRoomWidth + hallwayLength
houseBoundingZ1 = buildAreaZ1 + 7
houseBoundingZ2 = houseBoundingZ1 + lRoomDepth

# Porch Bounds
porchDepth = 5
porchBoundingX2 = houseBoundingX2
porchBoundingX1 = porchBoundingX2 - lRoomWidth
porchBoundingZ1 = houseBoundingZ1 - 5
porchBoundingZ2 = houseBoundingZ1

# Garage Bounds (for if it's present)
garageBoundingX1 = porchBoundingX2 + 1
garageBoundingX2 = garageBoundingX1 + garageWidth
garageBoundingZ1 = math.floor(houseBoundingZ2 - garageDepth)
garageBoundingZ2 = houseBoundingZ2

# Clear room area for house
# House proper
placeCuboid(editor, (houseBoundingX1, y, houseBoundingZ1),
           (houseBoundingX2, y + houseHeight, houseBoundingZ2), Block("air"))

# Porch
placeCuboid(editor, (porchBoundingX1, y, porchBoundingZ1),
           (porchBoundingX2, y + houseHeight, porchBoundingZ2), Block("air"))

# Garage
if garageHouse == 1:
    placeCuboid(editor, (garageBoundingX1, y, garageBoundingZ1),
               (garageBoundingX2, y + houseHeight, garageBoundingZ2), Block("air"))

# region BLOCK PALETTES
houseWalls = randint(0, 3)
if houseWalls == 0:
    houseWalls = ([
    Block ("quartz_block"),
    Block ("chiseled_quartz_block"),
    Block ("quartz_bricks"),
    Block ("quartz_pillar"),
    Block ("smooth_quartz")
    ])
elif houseWalls == 1:
    houseWalls = ([
    Block ("smooth_sandstone"),
    Block ("sandstone"),
    Block ("cut_sandstone"),
])
elif houseWalls == 2:
    houseWalls = ([
    Block ("stripped_oak_wood"),
    Block ("stripped_jungle_wood"),
])

else:
    houseWalls = ([
    Block ("smooth_red_sandstone"),
    Block ("red_sandstone"),
    Block ("cut_red_sandstone")
])

houseDoor = choice([
    "dark_oak_door",
    "spruce_door",
    "oak_door",
    "waxed_copper_door",
    "mangrove_door",
    "jungle_door",
    "acacia_door"
])

windowBlock = choice([
    Block("glass_pane"),
    Block("white_stained_glass_pane"),
    Block("light_gray_stained_glass_pane"),
    Block("gray_stained_glass_pane"),
    Block("black_stained_glass_pane"),
])

porchFloor = choice([
    Block("gray_terracotta"),
    Block("light_gray_terracotta"),
    Block("brown_terracotta"),
    Block("stripped_dark_oak_wood"),
    Block("stripped_spruce_wood"),
    Block("stripped_oak_wood")
])

foundationBlock = choice([
    Block("cobbled_deepslate"),
    Block("deepslate_bricks"),
    Block("deepslate_tiles"),
    Block("polished_blackstone_bricks")
])

roofBlock = choice([
    "dark_oak",
    "red_nether_brick",
    "mangrove",
    "spruce",
    "nether_brick",
])

porchFenceBlock = choice([
    "dark_oak",
    "oak",
    "spruce",
    "jungle",
    "crimson",
])

porchWall = choice([
    Block("dark_oak_planks"),
    Block("spruce_log"),
    Block("dark_oak_log"),
    Block("oak_log"),
    Block("black_terracotta"),
])
# endregion

# region BUILDING ROOMS

# region LIVINGROOM
# Coordinates
# Width
lRoomX1 = buildAreaX1 + hallwayLength + 2
lRoomX2 = lRoomX1 + lRoomWidth

# Depth
lRoomZ1 = buildAreaZ1 + porchDepth + 2
lRoomZ2 = lRoomZ1 + lRoomDepth

# Livingroom Palette
livingRoomFloor = choice([Block("white_terracotta"), Block("white_concrete"), 
                          Block("birch_planks"), Block("pale_oak_planks")])

# Livingroom Wall
placeCuboidHollow(editor, (lRoomX1, y, lRoomZ1), (lRoomX2, y + houseHeight, lRoomZ2), houseWalls)

# Livingroom Floor
placeCuboidHollow(editor, (lRoomX1, y, lRoomZ1), (lRoomX2, y, lRoomZ2), livingRoomFloor)

# Livingroom Doors
# Add double doors + doorbell
editor.placeBlock((lRoomX1 + 2, y + 1, lRoomZ1), Block(houseDoor, {"facing": "south", "hinge": "right"}))
editor.placeBlock((lRoomX1 + 3, y + 1, lRoomZ1), Block(houseDoor, {"facing": "south", "hinge": "left"}))
editor.placeBlock((lRoomX1 + 4, y + 2, lRoomZ1 - 1), Block("bell", {"attachment": "single_wall", "facing": "south"}))

# LIVINGROOM WINDOWS
wallPlacement = 2

windowY1 = y + wallPlacement
windowY2 = y + houseHeight - 2

# Front
placeCuboidHollow(editor, (lRoomX1 + 5, windowY1, lRoomZ1), (lRoomX2, windowY2, lRoomZ1), windowBlock)

# Front flower pots
flower = ([Block("potted_dandelion"), Block("potted_poppy"), Block("potted_blue_orchid"), Block("potted_allium"),
           Block("potted_azure_bluet"), Block("potted_orange_tulip"), Block("oxeye_daisy"), Block("potted_cornflower"),
           Block("potted_lily_of_the_valley"), Block("potted_oak_sapling"), Block("potted_jungle_sapling")])
placeCuboidHollow(editor, (lRoomX1 + 5, windowY1 - 1, lRoomZ1 - 1), (lRoomX2 - 1, windowY1 - 1, lRoomZ1 - 1), Block("grass_block"))
placeCuboidHollow(editor, (lRoomX1 + 5, windowY1, lRoomZ1 - 1), (lRoomX2 - 1, windowY1, lRoomZ1 - 1), flower)
placeCuboidHollow(editor, (lRoomX1 + 5, windowY1 - 1, lRoomZ1 - 2), (lRoomX2 - 1, windowY1 - 1, lRoomZ1 - 2), Block(porchFenceBlock + "_trapdoor", {"facing": "north", "open": "true"}))
editor.placeBlock((lRoomX1 + 4, windowY1 - 1, lRoomZ1 - 1), Block(porchFenceBlock + "_trapdoor", {"facing": "west", "open": "true"}))
editor.placeBlock((lRoomX1, windowY1, lRoomZ1 - 1), Block("lantern"))

if houseHeight > 5:
    placeCuboidHollow(editor, (lRoomX1+2, y+4, lRoomZ1), (lRoomX1+3, y+4, lRoomZ1), windowBlock)

# Side
if garageHouse == 1:
    placeCuboidHollow(editor, (lRoomX2, windowY1, lRoomZ1), (lRoomX2, windowY2, int((lRoomZ1 * .7 + lRoomZ2 * 0.3)) - 1), windowBlock)
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
# Porch is placed after the porch roof is built
# Coordinates
# Width
porchX1 = lRoomX1
porchX2 = lRoomX2

# Depth
porchZ2 = lRoomZ1
porchZ1 = porchZ2 - porchDepth
# endregion

# region HALLWAY
# Coordinates
# Width
hallwayWidth  = 3
hallwayX1 = lRoomX1
hallwayX2 = hallwayX1 - hallwayLength

# Depth
hallwayZ1 = int((lRoomZ1 + lRoomZ2) / 2 - 2)
hallwayZ2 = hallwayZ1 + 3

# Hallway Palette
hallwayFloor = livingRoomFloor

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
bedroomFloor = choice([Block("spruce_planks"), Block("oak_planks")])

placeCuboidHollow(editor, (bedroom1X1, y, bedroom1Z1), (bedroom1X2, y + houseHeight, bedroom1Z2), houseWalls) 
placeCuboidHollow(editor, (bedroom1X1, y, bedroom1Z1), (bedroom1X2, y, bedroom1Z2), bedroomFloor) 

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

placeCuboidHollow(editor, (bedroom2X1, y, bedroom2Z1), (bedroom2X2, y + houseHeight, bedroom2Z2), houseWalls) 
placeCuboidHollow(editor, (bedroom2X1, y, bedroom2Z1), (bedroom2X2, y, bedroom2Z2), bedroomFloor)

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

    placeCuboidHollow(editor, (bedroom3X1, y, bedroom3Z1), (bedroom3X2, y + houseHeight, bedroom3Z2), houseWalls) 
    placeCuboidHollow(editor, (bedroom3X1, y, bedroom3Z1), (bedroom3X2, y, bedroom3Z2), bedroomFloor)

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
kitchenFloor1 = choice([Block("white_concrete"), Block("white_shulker_box"), Block("pale_oak_planks")])
kitchenFloor2 = choice([Block("black_concrete"), Block("black_shulker_box"), Block("dark_oak_planks")])

placeCuboidHollow(editor, (kitchenX1, y, kitchenZ1), (kitchenX2, y + houseHeight, kitchenZ2), houseWalls) 
placeCheckeredCuboid(editor, (kitchenX1, y, kitchenZ1), (kitchenX2, y, kitchenZ2), kitchenFloor1, kitchenFloor2)

# Windows
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

# Palette
bathroomWall = Block("green_concrete")
bathroomFloor = choice([Block("stone_bricks"), Block("quartz_bricks"), Block("polished_diorite")])

placeCuboidHollow(editor, (bathroomX1, y, bathroomZ1), (bathroomX2, y + houseHeight, bathroomZ2), houseWalls) 
placeCuboidHollow(editor, (bathroomX1, y, bathroomZ1), (bathroomX2, y, bathroomZ2), bathroomFloor) 

# Windows
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
    placeCuboidWireframe(editor, (houseRoofX1 + i, yy, houseRoofZ1 + i), (houseRoofX1 + i, yy, houseRoofZ2 - i), eastRoofBlock) # right
    placeCuboidWireframe(editor, (houseRoofX2 - i, yy, houseRoofZ1 + i), (houseRoofX2 - i, yy, houseRoofZ2 - i), westRoofBlock) # left
    
    placeCuboidWireframe(editor, (houseRoofX1 + i, yy, houseRoofZ1 + i), (houseRoofX2 - i, yy, houseRoofZ1 + i), southRoofBlock) # front
    placeCuboidWireframe(editor, (houseRoofX1 + i, yy, houseRoofZ2 - i), (houseRoofX2 - i, yy, houseRoofZ2 - i), northRoofBlock) # back
editor.placeBlock((porchX1 - 1, y + houseHeight, porchZ2 - 2), Block("air")) # Removes an extra visible stair
houseWidth = lRoomX2 - bedroom2X1 + 1
houseRoofWidth = houseWidth + 2 # + 2 is due to overhang

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
porchWidth = porchRoofX2 - porchRoofX1 + 1
print("porchWidth:", porchWidth)

for i in range(0, porchRoofHeight):
    yy = y +  houseHeight + i
    placeCuboidWireframe(editor, (porchRoofX1 + i, yy, porchRoofZ1 + i), (porchRoofX1 + i, yy, porchRoofZ1 + i + porchRoofHeight - 2), eastRoofBlock) # right
    if lRoomWidth == 7:
        placeCuboidWireframe(editor, (porchRoofX1 + i, yy, porchRoofZ1 + i), (porchRoofX1 + i, yy, porchRoofZ1 + i + porchRoofHeight - 1), eastRoofBlock) # right
    placeCuboidWireframe(editor, (porchRoofX2 - i, yy, porchRoofZ1 + i), (porchRoofX2 - i, yy, porchRoofZ2 - i), westRoofBlock) # left
    
    placeCuboidWireframe(editor, (porchRoofX1 + i, yy, porchRoofZ1 + i), (porchRoofX2 - i, yy, porchRoofZ1 + i), southRoofBlock) # front

if porchWidth % 2 == 1:
    placeCuboid(editor, (porchRoofX1 + porchRoofHeight - 1, y + houseHeight + porchRoofHeight - 1, porchRoofZ1 + porchRoofHeight - 1),
                (porchRoofX1 + porchRoofHeight - 1, y + houseHeight + porchRoofHeight - 1, porchRoofZ1 + porchRoofHeight * 2 - 4),
                Block(roofBlock + "_slab"))
# endregion

# region PORCH PLACEMENT
# porch fences
placeCuboid(editor, (porchX1, y + 1, porchZ1),
                  (porchX2, y + 1, porchZ1), Block(porchFenceBlock + "_fence"))
placeCuboid(editor, (porchX2, y + 1, porchZ1),
                  (porchX2, y + 1, porchZ2), Block(porchFenceBlock + "_fence"))
placeCuboid(editor, (porchX1, y + 1, porchZ1),
                  (porchX1, y + 1, porchZ2), Block(porchFenceBlock + "_fence"))

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

# region GARAGE
# Coordinates
# Width
garageX1 = lRoomX2 + 1
garageX2 = garageX1 + garageWidth

# Depth
garageZ1 = int((lRoomZ1 * .7 + lRoomZ2 * 0.3))
garageZ2 = lRoomZ2

# Garage Palette
garageWall = randint(0, 2)
if garageWall == 0:
    garageWall = ([Block("polished_deepslate"), Block("deepslate_bricks"), Block("cracked_deepslate_bricks")])
elif garageWall == 1:
    garageWall = ([Block("blackstone"), Block("polished_blackstone"),
                   Block("polished_blackstone_bricks"), Block("cracked_polished_blackstone_bricks")])
else:
    garageWall = ([Block("stone"), Block("cobblestone"),
                   Block("stone_bricks"), Block("cracked_stone_bricks")])
garageFloor = Block("gray_wool")
garageDoor = Block(houseDoor, {"facing": "east", "hinge": "right"})

# Garage Wall + Door
garageDoorBlock = choice(["waxed_copper_trapdoor", "iron_trapdoor", "acacia_trapdoor"])

if garageHouse == 1:
    placeCuboidHollow(editor, (garageX1, y, garageZ1), (garageX2, y + houseHeight, garageZ2), garageWall)
    editor.placeBlock((garageX1, y+1, garageZ2 - 2), garageDoor)
    placeCuboidHollow(editor, (garageX1 - 1, y+1, garageZ2 - 2), (garageX1 - 1, y + 2, garageZ2 - 2), Block("air"))
    garageLeftX1 = garageX2 - 1
    garageRightX1 = garageX1 + 1

    if garageDoorsOpen == 0:
        garageBigDoors = Block(garageDoorBlock, {"facing": "south", "half": "bottom", "open": "true"})
        garageLeftX2 = garageLeftX1 - garageDoorWidth
        garageRightX2 = garageRightX1 + garageDoorWidth

        # Left Big Door
        placeCuboidHollow(editor, (garageLeftX1, y + 1, garageZ1),
                        (garageLeftX2, y +  houseHeight - 1, garageZ1), garageBigDoors)

        # Right Big Door
        placeCuboidHollow(editor, (garageRightX1, y + 1, garageZ1),
                        (garageRightX2, y +  houseHeight - 1, garageZ1), garageBigDoors)

    else:
        garageLeftDoors = Block(garageDoorBlock, {"facing": "west", "half": "bottom", "open": "true"})
        garageRightDoors = Block(garageDoorBlock, {"facing": "east", "half": "bottom", "open": "true"})
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

# region CAR
if garageHouse == 1:
    carX1 = garageX1 + 3
    carZ1 = garageZ1 + 3

    carX2 = carX1 + 2
    carZ2 = carZ1 + 3

    carBody = Block("dark_oak_slab" ,{"type": "top"})
    onFloorY = y + 1

    carNo = randint(0, 7)
    carColourPalette = (["white", "brown", "red", "orange",
                        "yellow", "cyan", "purple", "pink"])
    carTerracotta = Block(carColourPalette[carNo] + "_terracotta")

    carSlabPalette = (["pale_oak", "dark_oak", "mangrove", "acacia",
                    "bamboo", "warped", "crimson", "mangrove"])
    carSlab = Block(carSlabPalette[carNo] + "_slab", {"type": "top"})

    placeCuboidWireframe(editor, (carX1, onFloorY, carZ1), (carX2, onFloorY, carZ2), carBody)
    editor.placeBlock((carX1, onFloorY, carZ1), Block("black_"))
    editor.placeBlock((carX1, onFloorY, carZ2), Block("black_wool"))
    editor.placeBlock((carX2, onFloorY, carZ1), Block("black_wool"))
    editor.placeBlock((carX2, onFloorY, carZ2), Block("black_wool"))

    editor.placeBlock((carX1 - 1, onFloorY, carZ1), Block("stone_button", {"facing": "west"}))
    editor.placeBlock((carX1 - 1, onFloorY, carZ2), Block("stone_button", {"facing": "west"}))
    editor.placeBlock((carX2 + 1, onFloorY, carZ1), Block("stone_button", {"facing": "east"}))
    editor.placeBlock((carX2 + 1, onFloorY, carZ2), Block("stone_button", {"facing": "east"}))

    editor.placeBlock((carX1, onFloorY, carZ2 + 1), Block("hopper", {"facing": "north"}))
    editor.placeBlock((carX2, onFloorY, carZ2 + 1), Block("hopper", {"facing": "north"}))

    placeCuboid(editor, (carX1, onFloorY, carZ1 - 1), (carX2, onFloorY, carZ1 - 1), carBody)
    placeCuboid(editor, (carX1, onFloorY + 1, carZ1 - 1), (carX1, onFloorY + 1, carZ2 + 1), carTerracotta)
    placeCuboid(editor, (carX1 + 1, onFloorY + 1, carZ1 - 1), (carX1 + 1, onFloorY + 1, carZ2 + 1), carTerracotta)
    placeCuboid(editor, (carX2, onFloorY + 1, carZ1 - 1), (carX2, onFloorY + 1, carZ2 + 1), carTerracotta)

    editor.placeBlock((carX1, onFloorY + 1, carZ1 + 5), Block("mangrove_button", {"facing": "south"}))
    editor.placeBlock((carX2, onFloorY + 1, carZ1 + 5), Block("mangrove_button", {"facing": "south"}))

    editor.placeBlock((carX1, onFloorY + 1, carZ1 - 2), Block("pale_oak_button", {"facing": "north"}))
    editor.placeBlock((carX2, onFloorY + 1, carZ1 - 2), Block("pale_oak_button", {"facing": "north"}))

    editor.placeBlock((carX1 + 1, onFloorY + 2, carZ1 - 1), Block(carColourPalette[carNo] + "_carpet"))
    editor.placeBlock((carX1 + 1, onFloorY + 1, carZ1 - 2), Block("bamboo_wall_sign", {"facing": "north"}))
    editor.placeBlock((carX1 + 1, onFloorY + 1, carZ2 + 2), Block("bamboo_wall_sign", {"facing": "south"}))

    editor.placeBlock((carX1, onFloorY + 1, carZ1), carSlab)
    editor.placeBlock((carX1, onFloorY + 1, carZ2), carSlab)
    editor.placeBlock((carX2, onFloorY + 1, carZ1), carSlab)
    editor.placeBlock((carX2, onFloorY + 1, carZ2), carSlab)

    placeCuboid(editor, (carX1, onFloorY + 2, carZ1), (carX2, onFloorY + 2, carZ1 + 1), Block("light_gray_stained_glass"))
    placeCuboid(editor, (carX1, onFloorY + 3, carZ1), (carX2, onFloorY + 3, carZ1 + 1), Block("gray_carpet"))
# endregion

# endregion

# region FOUNDATION
houseX2 = lRoomX2
houseZ2 = lRoomZ2

# Main House
placeCuboidHollow(editor, (bedroom2X1, y - 20, lRoomZ1), (houseX2, y - 1, houseZ2), foundationBlock)
placeCuboidWireframe(editor, (bedroom2X1, y, lRoomZ1), (houseX2, y, houseZ2), foundationBlock)

# Garage Foundation
if garageHouse == 1:
    placeCuboidHollow(editor, (garageX1, y - 20, garageZ1), (garageX2, y - 1, garageZ2), foundationBlock)
    placeCuboidWireframe(editor, (garageX1, y, garageZ1), (garageX2, y, garageZ2), foundationBlock)

# Porch Foundation
placeCuboidHollow(editor, (porchX1, y - 20, porchZ1), (porchX2, y - 1, porchZ2), foundationBlock)
placeCuboidWireframe(editor, (porchX1, y, porchZ1), (porchX2, y, porchZ2), foundationBlock)

# porch staircase
for i in range (0, 10):
    block = editor.getBlock((porchX1 - i - 1, y - i, porchZ1 + 2))
    if block == Block("minecraft:air") or block == Block("minecraft:short_grass") or block == Block("minecraft:replaceable_by_trees"):
        editor.placeBlock((porchX1 - i - 1, y - i, porchZ1 + 2), Block(roofBlock + "_stairs", {"facing": "east"}))
        editor.placeBlock((porchX1 - i - 1, y - i - 1, porchZ1 + 2), foundationBlock)

    block = editor.getBlock((porchX1 - i - 1, y - i, porchZ1 - 2))
    if block == Block("minecraft:air") or block == Block("minecraft:short_grass") or block == Block("minecraft:replaceable_by_trees"):
        editor.placeBlock((porchX1 - i - 1, y - i, porchZ2 - 2), Block(roofBlock + "_stairs", {"facing": "east"}))
        editor.placeBlock((porchX1 - i - 1, y - i - 1, porchZ2 - 2), foundationBlock)
# endregion
# endregion

# region LIGHTING
lightingBlock = choice([Block("ochre_froglight"), Block("verdant_froglight"),
                        Block("pearlescent_froglight"), Block("sea_lantern")])

# Hallway Lights
# Midway livingroom
placeCuboid(editor, (hallwayX1 + lRoomWidth - 1, y + houseHeight, hallwayZ1 + 1), (hallwayX1 + lRoomWidth - 1, y + houseHeight, hallwayZ2 - 1), lightingBlock)

# Start hallway
placeCuboid(editor, (hallwayX1 + 1, y + houseHeight, hallwayZ1 + 1), (hallwayX1, y + houseHeight, hallwayZ2 - 1), lightingBlock)

# End hallway
placeCuboid(editor, (hallwayX2 + 1, y + houseHeight, hallwayZ1 + 1), (hallwayX2 + 1, y + houseHeight, hallwayZ2 - 1), lightingBlock)

def addCornerLighting(x1: int, z1: int, x2: int, z2: int):
    placeCuboid(editor, (x1 + 1, y + houseHeight, z1 + 1), (x1 + 2, y + houseHeight, z1 + 1), lightingBlock)
    editor.placeBlock((x1 + 1, y + houseHeight, z1 + 2), lightingBlock)

    placeCuboid(editor, (x2 - 1, y + houseHeight, z1 + 1), (x2 - 2, y + houseHeight, z1 + 1), lightingBlock)
    editor.placeBlock((x2 - 1, y + houseHeight, z1 + 2), lightingBlock)
    
    placeCuboid(editor, (x1 + 1, y + houseHeight, z2 - 1), (x1 + 2, y + houseHeight, z2 - 1), lightingBlock)
    editor.placeBlock((x1 + 1, y + houseHeight, z2 - 2), lightingBlock)

    placeCuboid(editor, (x2 - 1, y + houseHeight, z2 - 1), (x2 - 2, y + houseHeight, z2 - 1), lightingBlock)
    editor.placeBlock((x2 - 1, y + houseHeight, z2 - 2), lightingBlock)

# Livingroom Lights
addCornerLighting(lRoomX1, lRoomZ1, lRoomX2, lRoomZ2)

# Bedroom Lights
addCornerLighting(bedroom1X1, bedroom1Z1, bedroom1X2, bedroom1Z2)
addCornerLighting(bedroom2X1, bedroom2Z1, bedroom2X2, bedroom2Z2)
if hallwayLength >= 15:
    addCornerLighting(bedroom3X1, bedroom3Z1, bedroom3X2, bedroom3Z2) # type: ignore

# Kitchen Lights
addCornerLighting(kitchenX1, kitchenZ2, kitchenX2, kitchenZ1)

# Bathroom Lights
addCornerLighting(bathroomX1, bathroomZ2, bathroomX2, bathroomZ1)

# Garage Lights
garageLightY = y + houseHeight - 1
garageLightBlock = choice([Block("lantern"), Block("waxed_copper_lantern"), Block("waxed_oxidized_copper_lantern"),
                           Block("end_rod", {"facing": "down"})])
if garageHouse == 1:
    editor.placeBlock((garageX1 + 1, garageLightY, garageZ1 + 1), garageLightBlock)
    editor.placeBlock((garageX2 - 1, garageLightY, garageZ1 + 1), garageLightBlock)
    editor.placeBlock((garageX1 + 1, garageLightY, garageZ2 - 1), garageLightBlock)
    editor.placeBlock((garageX2 - 1, garageLightY, garageZ2 - 1), garageLightBlock)
# endregion

# region FURNITURE

# region PALETTE
chairWood = choice([
    "oak",
    "birch",
    "acacia",
    "mangrove",
    "cherry",
    "pale_oak",
    "crimson"
])

chairArmWood = choice([
    "dark_oak",
    "spruce",
    "birch",
    "mangrove",
    "cherry",
    "pale_oak",
    "crimson",
])

while chairWood == chairArmWood:
    chairArmWood = choice([
    "dark_oak",
    "spruce",
    "birch",
    "mangrove",
    "cherry",
    "pale_oak",
    "crimson",
    ])

# Painting colour associations
redPaintings = ["donkey_kong"]
orangePaintings = ["skeleton", "finding"]
yellowPaintings = ["changing", "wasteland", "alban", "bomb", "kebab"]
greenPaintings = ["aztec2", "plant", "fighters", "dennis"]
lightBluePaintings = ["creebet", "sea", "meditative", "pool", "tides"]
purplePaintings = ["sunset", "lowmist"]
grayPaintings = ["passage", "aztec", "courbet", "endboss"]
brownPaintings = ["bouquet", "cavebird", "cotan", "fern",
                  "owlemons", "sunflowers"]


def chooseAccentColour(painting: str):
    global accentColour 
    if painting in redPaintings:
        accentColour = choice(["red", "black", "light_gray", "white"])

    elif painting in orangePaintings:
        accentColour = choice(["orange", "white", "light_gray", "brown", "gray"])

    elif painting in yellowPaintings:
        accentColour = choice(["orange", "yellow", "lime", "green"])
    
    elif painting in greenPaintings:
        accentColour = choice(["green", "white", "light_gray"])
    
    elif painting in lightBluePaintings:
        accentColour = choice(["light_blue"])
    
    elif painting in purplePaintings:
        accentColour = choice(["cyan", "blue", "purple"])
    
    elif painting in grayPaintings:
        accentColour = choice(["white", "light_gray", "gray"])

    elif painting in brownPaintings:
        accentColour = choice(["brown", "yellow"])


    else:
        accentColour = choice(["magenta"])
# endregion

# region Livingroom
bannerY = y
onFloorY = y + 1

# Dining Chair def    slab coords,    tradoor coords,   banner direction,  trapdoor direction
def placeDiningChairs(x: int, z: int, xT: int, zT: int, bannerFacing: str, trapdoorFacing: str):
    # Slab
    editor.placeBlock((x, onFloorY, z), Block(chairWood + "_slab", {"type": "bottom"}))

    # Trapdoors
    editor.placeBlock((xT, onFloorY, zT), Block(chairWood + "_trapdoor", {"facing": trapdoorFacing, "open": "true"}))
    editor.placeBlock((xT, onFloorY + 1, zT), Block(chairWood + "_trapdoor", {"facing": trapdoorFacing, "open": "true"}))

    # Banner
    editor.placeBlock((x, onFloorY + 1, z), Block(accentColour + "_wall_banner", {"facing": bannerFacing}))

# Door couch dimensions
couchDX1 = lRoomX1 + 4 # corner next to door
couchDX2 = lRoomX2 - 2 # next to wall corner

couchDZ1 = lRoomZ1 + 1 # corner next to door

# Right-side couch dimensions
couchRX1 = lRoomX1 + 3 # side next to door

couchRZ1 = lRoomZ1 + 3 # side next to door
couchRZ2 = lRoomZ2 - 9 # far-end of couch

# Back couch dimensions
couchBX1 = lRoomX1 + 3 # hallway-side
couchBX2 = lRoomX2 - 2 # wall side
couchBZ1 = lRoomZ2 - 8 # depth

rightCouchLength = (lRoomZ2 - 9) - (lRoomZ1 + 3)

# TV
tvX = str(lRoomX2 - 1)
tvY = str(y + 3)
tvZ = str(couchRZ1)

if rightCouchLength == 1:
    tvScreen = choice([
    "kebab", "aztec", "alban", "aztec2", 
    "bomb", "plant", "wasteland", "meditative"
])
    tvY = str(y + 2)
    tvShelfHeight = 1
    
elif rightCouchLength == 2:
    tvScreen = choice([
    "pool", "courbet", "sunset", "sea", "creebet"
])
    tvY = str(y + 2)
    tvShelfHeight = 1
    
elif rightCouchLength == 3:
    tvScreen = choice([
    "bouquet", "cavebird", "cotan", "endboss", "fern",
    "owlemons", "sunflowers", "tides", "dennis"
])
    tvZ = str(couchRZ1 + 1)
    tvShelfHeight = 4
    
elif rightCouchLength == 4 and houseHeight == 5:
    tvScreen = choice([
    "fighters", "changing", "finding", "lowmist", "passage"
])  
    tvY = str(y + 2)
    tvZ = str(couchRZ1 + 1)
    tvShelfHeight = 3

else:
    tvScreen = choice([
    "skeleton", "donkey_kong"
])
    tvZ = str(couchRZ1 + 1)
    tvShelfHeight = 4
    
placeCuboid(editor, (lRoomX2 - 1, y + 2, couchRZ1 - 1), (lRoomX2 - 1, y + tvShelfHeight, couchRZ1 - 1),
            Block(chairArmWood + "_trapdoor", {"facing": "west", "open": "true"}))

placeCuboid(editor, (lRoomX2 - 1, y + 2, couchRZ2), (lRoomX2 - 1, y + tvShelfHeight, couchRZ2),
            Block(chairArmWood + "_trapdoor", {"facing": "west", "open": "true"}))

chooseAccentColour(tvScreen)
print("tvScreen Painting: ", tvScreen)

# Placing Chairs
def placeLRoomChairs(cX1: int, cZ1: int, cX2: int, cZ2: int, bannerFacing: int, chairFacing: str):
    # Chairs
    placeCuboid(editor, (cX1, onFloorY, cZ1), (cX2, onFloorY, cZ2), Block(chairWood + "_stairs", {"facing": chairFacing}))

    # Glowstone (to light banners)
    placeCuboidHollow(editor, (cX1, y - 1, cZ1), (cX2, y - 1, cZ2), Block("glowstone"))
    
    # Banners (couch pillows)
    placeCuboidHollow(editor, (cX1, bannerY, cZ1), (cX2, bannerY, cZ2), Block(accentColour + "_banner", {"rotation": bannerFacing}))

# Placing Trapdoors (Armrests)
def placeLRoomTrapdoors(tX1: int, tZ1: int, trapdoorFacing: str):
    editor.placeBlock((tX1, onFloorY, tZ1), Block(chairArmWood + "_trapdoor", {"facing": trapdoorFacing, "open": "true"}))

placeLRoomChairs(couchDX1, couchDZ1, couchDX2, couchDZ1, 0, "north")
placeLRoomTrapdoors(couchDX1 - 1, couchDZ1, "west") # next to door armrest
placeLRoomTrapdoors(couchDX2 + 1, couchDZ1, "east") # next to wall armrest

placeLRoomChairs(couchRX1, couchRZ1, couchRX1, couchRZ2, 12, "west")
placeLRoomTrapdoors(couchRX1, couchRZ1 - 1, "north") # door-side armrest

placeLRoomChairs(couchBX1, couchBZ1, couchDX2, couchBZ1, 8, "south")
placeLRoomTrapdoors(couchBX2 + 1, couchBZ1, "east") # wall-side armrest

# Remove corner banner
editor.placeBlock((couchRX1, bannerY, couchBZ1), Block("air"))

# Coffee Table
placeCuboid(editor, (couchBX1 + 2, onFloorY, couchRZ1), (couchBX2, onFloorY, couchRZ2 - 1),
            Block(chairArmWood + "_slab", {"type": "top"}))

 
# Decides dining room setup based on living room dimensions
if lRoomWidth == 7:
    diningSetup = 0
    diningTableX1 = lRoomX1 + 3
    diningTableX2 = diningTableX1
    diningTableZ1 = lRoomZ2 - 5
    diningTableZ2 = diningTableZ1 + 2

    # Chairs
    placeDiningChairs(diningTableX1, lRoomZ2 - 2, diningTableX1, lRoomZ2 - 1, "north", "south") # back
    placeDiningChairs(diningTableX1, lRoomZ2 - 6, diningTableX1, lRoomZ2 - 7, "south", "north") # front

    placeDiningChairs(diningTableX1 - 1, lRoomZ2 - 3, diningTableX1 - 2, lRoomZ2 - 3, "east", "west") # right - front
    placeDiningChairs(diningTableX1 - 1, lRoomZ2 - 5, diningTableX1 - 2, lRoomZ2 - 5, "east", "west") # right - back

    placeDiningChairs(diningTableX1 + 1, lRoomZ2 - 3, diningTableX1 + 2, lRoomZ2 - 3, "west", "east") # left - front
    placeDiningChairs(diningTableX1 + 1, lRoomZ2 - 5, diningTableX1 + 2, lRoomZ2 - 5, "west", "east") # left - back

elif ((lRoomWidth == 8 and (lRoomDepth == 13 or lRoomDepth == 14)) or
      (lRoomWidth == 9 and (lRoomDepth == 13 or lRoomDepth == 14))):
    diningSetup = 1
    diningTableX1 = lRoomX1 + 3
    diningTableX2 = diningTableX1 + 2
    diningTableZ1 = lRoomZ2 - 3
    diningTableZ2 = diningTableZ1
    
    # Chairs
    placeDiningChairs(diningTableX1 + 2, lRoomZ2 - 2, diningTableX1 + 2, lRoomZ2 - 1, "north", "south") # back - left
    placeDiningChairs(diningTableX1, lRoomZ2 - 2, diningTableX1, lRoomZ2 - 1, "north", "south") # back - right
    
    placeDiningChairs(diningTableX1 + 2, lRoomZ2 - 4, diningTableX1 + 2, lRoomZ2 - 5, "south", "north") # front - left
    placeDiningChairs(diningTableX1, lRoomZ2 - 4, diningTableX1, lRoomZ2 - 5, "south", "north") # front - right

    placeDiningChairs(diningTableX1 - 1, lRoomZ2 - 3, diningTableX1 - 2, lRoomZ2 - 3, "east", "west") # right
    placeDiningChairs(diningTableX1 + 3, lRoomZ2 - 3, diningTableX1 + 4, lRoomZ2 - 3, "west", "east") # left

else:
    diningSetup = 3
    diningTableX1 = lRoomX1 + 3
    diningTableX2 = diningTableX1 + 2
    diningTableZ1 = lRoomZ2 - 5
    diningTableZ2 = diningTableZ1 + 2

    # Chairs
    placeDiningChairs(diningTableX1 + 2, lRoomZ2 - 2, diningTableX1 + 2, lRoomZ2 - 1, "north", "south") # back - left
    placeDiningChairs(diningTableX1, lRoomZ2 - 2, diningTableX1, lRoomZ2 - 1, "north", "south") # back - right
    
    placeDiningChairs(diningTableX1 + 2, lRoomZ2 - 6, diningTableX1 + 2, lRoomZ2 - 7, "south", "north") # front - left
    placeDiningChairs(diningTableX1, lRoomZ2 - 6, diningTableX1, lRoomZ2 - 7, "south", "north") # front - right

    placeDiningChairs(diningTableX1 + 3, lRoomZ2 - 3, diningTableX1 + 4, lRoomZ2 - 3, "west", "east") # left - back
    placeDiningChairs(diningTableX1 + 3, lRoomZ2 - 5, diningTableX1 + 4, lRoomZ2 - 5, "west", "east") # left - front
    
    placeDiningChairs(diningTableX1 - 1, lRoomZ2 - 3, diningTableX1 - 2, lRoomZ2 - 3, "east", "west") # right - back
    placeDiningChairs(diningTableX1 - 1, lRoomZ2 - 5, diningTableX1 - 2, lRoomZ2 - 5, "east", "west") # right - front
  


placeCuboid(editor, (lRoomX2 - 1, y + 1, couchRZ1 - 1), (lRoomX2 - 1, y + 1, couchRZ2),
            Block(chairWood + "_shelf", {"facing": "west"}))
tvPos = str(tvX + " " + tvY + " " + tvZ)
tvCommand = ("summon minecraft:painting " + tvPos + " {facing:1,variant:'minecraft:" + tvScreen + "'}")
runCommand(tvCommand)

# endregion

# region Dining Room
# Building Dining Table
placeCuboid(editor, (diningTableX1, onFloorY, diningTableZ1),
            (diningTableX2, onFloorY, diningTableZ2), Block(chairArmWood + "_slab", {"type": "top"}))
plateX = diningTableX1
plateZ = diningTableZ1
# endregion

# region Kitchen
# Back
editor.placeBlock((kitchenX1 + 2, onFloorY, kitchenZ2), Block(houseDoor, {"facing": "south", "hinge": "right"}))
placeCuboid(editor, (kitchenX1 + 1, onFloorY, kitchenZ1 - 1), (kitchenX2 - 1, onFloorY, kitchenZ1 - 1), Block("barrel", {"facing": "north"}))
editor.placeBlock((kitchenX1 + 2, onFloorY, kitchenZ1 - 1), Block("water_cauldron", {"level": "3"}))
editor.placeBlock((kitchenX1 + 3, onFloorY + 1, kitchenZ1 - 1), flower)

# Left Side
placeCuboid(editor, (kitchenX2 - 1, onFloorY, kitchenZ2 + 1), (kitchenX2 - 1, onFloorY, kitchenZ1 - 1), Block(chairWood + "_planks"))
placeCuboid(editor, (kitchenX2 - 1, onFloorY + 2, kitchenZ2 + 1), (kitchenX2 - 1, onFloorY + 2, kitchenZ1 - 1), Block("barrel", {"facing": "west"}))
editor.placeBlock((kitchenX2 - 1, onFloorY, kitchenZ2 + 2), Block("furnace", {"facing": "west"}))
editor.placeBlock((kitchenX2 - 1, onFloorY, kitchenZ2 + 3), Block("furnace", {"facing": "west"}))

# Corner Fridge
placeCuboid(editor, (kitchenX2 - 1, onFloorY, kitchenZ2 + 1), (kitchenX2 - 1, onFloorY + 1, kitchenZ2 + 1), Block("iron_block"))
# endregion

# region Bathroom
editor.placeBlock((bathroomX1 + 1, onFloorY + 1, bathroomZ1 - 1), Block("smooth_quartz"))
editor.placeBlock((bathroomX1 + 1, onFloorY, bathroomZ1 - 1), Block("smooth_quartz_stairs", {"facing": "north", "half": "top"}))
editor.placeBlock((bathroomX1 + 1, onFloorY, bathroomZ1 - 2), Block("smooth_quartz_stairs", {"facing": "south", "half": "top"}))
editor.placeBlock((bathroomX1 + 1, onFloorY + 1, bathroomZ1 - 2), Block("white_wall_banner", {"facing": "north"}))
editor.placeBlock((bathroomX2 - 1, y + houseHeight - 1, bathroomZ1 - 1), Block("iron_chain", {"axis": "y"}))
editor.placeBlock((bathroomX2 - 1, y + houseHeight - 2, bathroomZ1 - 1), Block("iron_chain", {"axis": "y"}))
editor.placeBlock((bathroomX2 - 1, y + houseHeight - 3, bathroomZ1 - 1), Block("pale_oak_trapdoor", {"facing": "north", "half": "top"}))
  
editor.placeBlock((bathroomX2 - 1, onFloorY, bathroomZ2 + 2), Block("smooth_quartz_stairs", {"facing": "east", "half": "top"}))
editor.placeBlock((bathroomX2 - 1, onFloorY + 1, bathroomZ2 + 2), Block("light_blue_wall_banner", {"facing": "west"}))

editor.placeBlock((bathroomX1 + 2, onFloorY, bathroomZ2), Block(houseDoor, {"facing": "south", "hinge": "left"}))
# endregion

# region Bedrooms
# region Bedroom #1

# Bunk bed
placeCuboid(editor, (bedroom1X2 - 1, onFloorY, bedroom1Z1 + 1), (bedroom1X2 - 2, onFloorY, bedroom1Z1 + 1), Block("chest", {"facing": "south"}))
editor.placeBlock((bedroom1X2 - 1, onFloorY, bedroom1Z1 + 1), Block("chest", {"facing": "south", "type": "left"}))
editor.placeBlock((bedroom1X2 - 2, onFloorY, bedroom1Z1 + 1), Block("chest", {"facing": "south", "type": "right"}))
placeCuboid(editor, (bedroom1X2 - 1, onFloorY + 1, bedroom1Z2 - 1), (bedroom1X2 - 2, onFloorY + 1, bedroom1Z2 - 1), Block(chairWood + "_slab", {"type": "top"}))
placeCuboid(editor, (bedroom1X2 - 1, onFloorY, bedroom1Z2 - 2), (bedroom1X2 - 1, onFloorY + 1, bedroom1Z2 - 2), Block("ladder", {"facing": "west"}))
editor.placeBlock((bedroom1X2 - 2, onFloorY + 2, bedroom1Z2 - 1), Block(accentColour + "_bed", {"facing": "east"}))
editor.placeBlock((bedroom1X2 - 2, onFloorY, bedroom1Z2 - 1), Block(accentColour + "_bed", {"facing": "east"}))
placeCuboid(editor, (bedroom1X2 - 1, onFloorY + 2, bedroom1Z2 - 2), (bedroom1X2 - 2, onFloorY + 2, bedroom1Z2 - 2), Block(chairWood + "_wall_sign", {"facing": "north"}))
editor.placeBlock((bedroom1X2 - 3, onFloorY + 2, bedroom1Z2 - 1), Block(chairWood + "_wall_sign", {"facing": "west"}))

# Desk
editor.placeBlock((bedroom1X1 + 1, onFloorY, bedroom1Z1 + 1), Block(chairWood + "_stairs", {"half": "top", "facing": "north"}))
editor.placeBlock((bedroom1X1 + 1, onFloorY, bedroom1Z1 + 2), Block(chairWood + "_slab", {"type": "top"}))
editor.placeBlock((bedroom1X1 + 1, onFloorY, bedroom1Z1 + 3), Block(chairWood + "_stairs", {"half": "top", "facing": "south"}))
placeCuboid(editor, (bedroom1X1 + 1, onFloorY + 1, bedroom1Z1 + 1), (bedroom1X1 + 1, onFloorY + 1, bedroom1Z1 + 3), Block(accentColour + "_carpet"))

# Chair
editor.placeBlock((bedroom1X1 + 2, onFloorY, bedroom1Z1 + 2), Block(chairWood + "_stairs", {"half": "bottom", "facing": "east"}))

# Door
editor.placeBlock((bedroom1X1 + 2, onFloorY, bedroom1Z2), Block(houseDoor, {"hinge": "left", "facing": "north"}))

# endregion

# region Bedroom #2
# Desk
editor.placeBlock((bedroom2X2 - 1, onFloorY, bedroom2Z1 + 1), Block(chairWood + "_stairs", {"half": "top", "facing": "north"}))
editor.placeBlock((bedroom2X2 - 1, onFloorY, bedroom2Z1 + 2), Block(chairWood + "_slab", {"type": "top"}))
editor.placeBlock((bedroom2X2 - 1, onFloorY, bedroom2Z1 + 3), Block(chairWood + "_stairs", {"half": "top", "facing": "south"}))
placeCuboid(editor, (bedroom2X2 - 1, onFloorY + 1, bedroom2Z1 + 1), (bedroom2X2 - 1, onFloorY + 1, bedroom2Z1 + 3), Block(accentColour + "_carpet"))

# Chair
editor.placeBlock((bedroom2X2 - 2, onFloorY, bedroom2Z1 + 2), Block(chairWood + "_stairs", {"half": "bottom", "facing": "west"}))

# Bed
placeCuboid(editor, (bedroom2X1 + 1, onFloorY, bedroom2Z2 - 1), (bedroom2X1 + 1, onFloorY, bedroom2Z2 - 4), Block("barrel", {"facing": "east"}))
placeCuboid(editor, (bedroom2X1 + 2, onFloorY, bedroom2Z2 - 2), (bedroom2X1 + 2, onFloorY, bedroom2Z2 - 3), Block(accentColour + "_bed", {"facing": "west"}))
editor.placeBlock((bedroom2X1 + 1, onFloorY + 1, bedroom2Z2 - 1), Block("lantern"))
editor.placeBlock((bedroom2X1 + 1, onFloorY + 1, bedroom2Z2 - 4), flower)

# Door
editor.placeBlock((bedroom2X2 - 2, onFloorY, bedroom2Z2), Block(houseDoor, {"hinge": "right", "facing": "north"}))
# endregion

# region Bedroom #3
if hallwayLength >= 15:
    # Bed
    placeCuboid(editor, (bedroom3X1 + 1, onFloorY, bedroom3Z2 - 1), (bedroom3X1 + 1, onFloorY, bedroom3Z2 - 4), Block("barrel", {"facing": "east"})) # type: ignore
    placeCuboid(editor, (bedroom3X1 + 2, onFloorY, bedroom3Z2 - 2), (bedroom3X1 + 2, onFloorY, bedroom3Z2 - 3), Block(accentColour + "_bed", {"facing": "west"})) # type: ignore
    editor.placeBlock((bedroom3X1 + 1, onFloorY + 1, bedroom3Z2 - 1), Block("lantern")) # type: ignore
    editor.placeBlock((bedroom3X1 + 1, onFloorY + 1, bedroom3Z2 - 4), flower) # type: ignore

    # Chest
    editor.placeBlock((bedroom3X2 - 1, onFloorY, bedroom3Z1 + 1), Block("chest", {"facing": "west"})) # type: ignore

    # Door
    editor.placeBlock((bedroom3X2 - 2, onFloorY, bedroom3Z1), Block(houseDoor, {"facing": "south", "hinge": "left"})) # type: ignore
# endregion
# endregion
# endregion


runCommand("tp Snazziington " + tvPos)
print("tp Snazziington " + tvPos)