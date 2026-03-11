import math, statistics
from random import randint, choice
from gdpc import Editor, Block #, Transform
from gdpc.geometry import placeCuboid, placeCuboidHollow, placeRectOutline, placeCuboidWireframe

editor = Editor(buffering=True)

# 1. Load a WorldSlice with Editor.loadWorldSlice()
worldSlice = editor.loadWorldSlice() # Loads the build area by default

# 2. Specify the area to load explicitly
buildArea = editor.getBuildArea()
buildRect = buildArea.toRect() # Converts a 3D Box to its XZ-rect

buildAreaX1 = buildArea.offset.x + 1
buildAreaZ1 = buildArea.offset.z + 1
worldSlice = editor.loadWorldSlice()

# 3. Store the WorldSlice in the Editor
editor.loadWorldSlice(buildRect, cache=True)

# House Dimensions
hallwayLength = randint(10, 18) # length of hallway. if > 15, third bedroom spawns
print("hallwayLength: ", hallwayLength)

houseHeight = randint(5, 7) # determines height of house
print("houseHeight: ", houseHeight)

lRoomDepth = randint(13, 16) # livingRoom depth
print("lRoomDepth: ", lRoomDepth)

lRoomWidth = randint(7, 9) # livingRoom width
print("lRoomWidth: ", lRoomWidth)

garageWidth = choice([7, 9])
garageDepth = math.floor(lRoomDepth * .7)
print("garageWidth: ", garageWidth)
print("garageDepth: ", garageDepth)
garageDoorWidth = math.floor((garageWidth - 2) / 2)

# House Bounds
houseBoundingX1 = buildAreaX1 - hallwayLength
houseBoundingX2 = buildAreaX1 + lRoomWidth
houseBoundingZ1 = buildAreaZ1
houseBoundingZ2 = buildAreaZ1 + lRoomDepth

# Porch Bounds
porchBoundingX1 = buildAreaX1
porchBoundingX2 = buildAreaX1 + lRoomWidth
porchBoundingZ1 = houseBoundingZ1 - 5
porchBoundingZ2 = houseBoundingZ1

# Garage Bounds (for if it's present)
garageBoundingX1 = porchBoundingX2 + 1
garageBoundingX2 = garageBoundingX1 + garageWidth
garageBoundingZ1 = math.floor(houseBoundingZ2 - garageDepth)
garageBoundingZ2 = houseBoundingZ2

# Total
houseTotalWidth = garageWidth + lRoomWidth + hallwayLength
houseTotalDepth = lRoomDepth + (porchBoundingZ2 - porchBoundingZ1)
print("houseTotalWidth: ", houseTotalWidth)
print("houseTotalDepth: ", houseTotalDepth)

placeRectOutline(editor, buildArea.toRect(), 72, Block("red_concrete"))

global heightMapList
heightMapList = []

global heightMapAverages
heightMapAverages = []

global flattestLandCoords
flattestLandCoords = []

lowestStdDev = 10
pillarHeight = 1

# region HOUSE PLACEMENT
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
            lowestStdDev = newStdDev
            global lowestX
            lowestX = x

            global lowestZ
            lowestZ = z
            print("Changed to ", lowestStdDev)
            print("lowestX: ", lowestX, "lowestZ: ", lowestZ)
            global pillarHeight
            pillarHeight += 1
            y = int(heightmap[lowestX, lowestZ] + 2) + 20
            print("Placing Block here:", (lowestX + buildArea.offset.x, y, lowestZ + buildArea.offset.z))
            placeCuboidWireframe(editor, (lowestX + buildArea.offset.x, y, lowestZ + buildArea.offset.z),
                                (lowestX + buildArea.offset.x + houseTotalWidth, y + pillarHeight, lowestZ + buildArea.offset.z + houseTotalDepth),
                                Block("redstone_block"))

for x in range (0, 100 - houseTotalWidth):
    if x % 10 == 0:
        for z in range (0, 100 - houseTotalDepth):
            if z % 10 == 0:
                calcHeightMap(x, z)
                print("X, Z:", x, z)
print("Lowest stdDev is found at: ", lowestX, lowestZ)