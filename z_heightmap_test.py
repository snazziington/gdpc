import math
from random import randint, choice
from gdpc import Editor, Block #, Transform
from gdpc.geometry import placeCuboid, placeCuboidHollow, placeRectOutline, placeCuboidWireframe

editor = Editor(buffering=True)

# 1. Load a WorldSlice with Editor.loadWorldSlice()
worldSlice = editor.loadWorldSlice() # Loads the build area by default

# 2. Specify the area to load explicitly
buildArea = editor.getBuildArea()
print(buildArea)
buildRect = buildArea.toRect() # Converts a 3D Box to its XZ-rect

x = buildArea.offset.x + 1
z = buildArea.offset.z + 1
worldSlice = editor.loadWorldSlice()

# 3. Store the WorldSlice in the Editor
editor.loadWorldSlice(buildRect, cache=True)

# Get heightmap
heightmap = editor.worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"] # type: ignore

print(heightmap)


y = heightmap[100, 100]
print(y)
placeRectOutline(editor, buildArea.toRect(), 67, Block("red_concrete"))

# region HOUSE PLACEMENT


# y = house floor height
# y = heightmap[1, 1]# + 3 is temporary while i do blueprints

# Max width is 40, Max depth is 25
# So I need to check width across 8 of the blocks
# And check depth across 5

# For the entire build area
for x in range (0, 60):
    #print("X: ", x)
    for z in range (0, 75):
        #print("Z: ", z)
        #print(y)
        if z % 5 == 0 and x % 5 == 0:
            xBlock = buildArea.offset.x + x
            zBlock = buildArea.offset.z + z
            y = heightmap[x, z] + 1
            print(x, y, z)
            palette = choice([Block("red_stained_glass"), Block("orange_stained_glass"), Block("yellow_stained_glass"),
                            Block("green_stained_glass"), Block("blue_stained_glass"), Block("purple_stained_glass"), Block("pink_stained_glass")])
            placeCuboid(editor, (xBlock, y, zBlock), (xBlock - 4, y + 1, zBlock - 4), palette)
        #if z % 5 == 0 and x % 5 == 0:
        # So for every 5 blocks in the buildArea


"""
I should do something like
For the entire build area.
Check every 40x25 area for the lowest absolute value. Starting from x1 and x2.
At this lowets absolute value point, put a glowstone pillar.
"""