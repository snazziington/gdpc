from random import randint, choice
from gdpc import Editor, Block
from gdpc.geometry import placeCuboid, placeCuboidHollow, placeCuboidWireframe

editor = Editor(buffering=True)

buildArea = editor.getBuildArea()

# region Deciding Floor Level

# Load world slice of the build area
editor.loadWorldSlice(cache=True)

# Get heightmap
heightmap = editor.worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

# i guess y is equal to the average heighmap??????? idk man
y = heightmap[5,5] + 1
# endregion

# region CAR
carX1 = buildArea.offset.x + 1 # 
carZ1 = buildArea.offset.z + 1

carX2 = carX1 + 2
carZ2 = carZ1 + 3

carBody = Block("dark_oak_slab" ,{"type": "top"})
onFloorY = y + 1

carNo = randint(0, 10)
carColourPalette = (["white", "gray", "black", "brown", "red", "orange",
                     "yellow", "cyan", "purple", "magenta", "pink"])
carTerracotta = Block(carColourPalette[carNo] + "_terracotta")

carSlabPalette = (["pale_oak", "nether_brick", "nether_brick", "dark_oak", "mangrove", "acacia",
                   "bamboo", "warped", "crimson", "crimson", "mangrove"])
carSlab = Block(carSlabPalette[carNo] + "_slab", {"type": "top"})

placeCuboidWireframe(editor, (carX1, onFloorY, carZ1), (carX2, onFloorY, carZ2), carBody)
editor.placeBlock((carX1, onFloorY, carZ1), Block("black_wool"))
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