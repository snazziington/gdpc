import math
from random import randint, choice
from gdpc import Editor, Block #, Transform
from gdpc.geometry import placeCuboid, placeCuboidHollow, placeRectOutline, placeCuboidWireframe

editor = Editor(buffering=True)

buildArea = editor.getBuildArea()

# Load world slice of the build area
editor.loadWorldSlice(cache=True)

heightmap = editor.worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"] # type: ignore

# y = house floor height
#y = heightmap[1, 1]# + 3 is temporary while i do blueprints

for x in range (buildArea.offset.x, buildArea.offset.x + 100):
    if x % 5 == 0:
        print("X: ", x)
    for z in range (buildArea.offset.z, buildArea.offset.z + 100):
        if z % 5 == 0:
            print("Z: ", z)
            print("Heightmap: ", heightmap[x, z])