import math
from random import randint, choice # type: ignore
from gdpc import Editor, Block, Transform
from gdpc.geometry import placeCuboid, placeCuboidHollow, placeRectOutline, placeCuboidWireframe

editor = Editor(buffering=True)

buildArea = editor.getBuildArea()

placeRectOutline(editor, buildArea.toRect(), 67, Block("red_concrete"))

# Finding floor
# Load world slice of the build area
editor.loadWorldSlice(cache=True)

# Get heightmap
heightmap = editor.worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"] # type: ignore

#  y = Foundation height
y = heightmap[0, 0] + 1 # + 3 is temporary while i do blueprints

# x & z coordinates to build the roof
x1 = buildArea.offset.x + 1
z1 = buildArea.offset.z + 1

x2 = buildArea.offset.x + 10
z2 = buildArea.offset.z + 10

# Clear area
placeCuboid(editor, (x1, y, z1), (x2, y + 10, z2), Block("air"))

height = randint(5, 6)

for i in range(1, 5):
    yy = y + i
    placeCuboidHollow(editor, (x1 + i, yy, z1 + i), (x2 - i, yy, z2 - i), Block("glass"))