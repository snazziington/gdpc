import math
from random import randint, choice # type: ignore
from gdpc import Editor, Block, Transform
from gdpc.geometry import placeCuboid, placeCuboidHollow, placeRectOutline

editor = Editor(buffering=True)

buildArea = editor.getBuildArea()

placeRectOutline(editor, buildArea.toRect(), 67, Block("red_concrete"))

# Finding floor
# Load world slice of the build area
editor.loadWorldSlice(cache=True)

# Get heightmap
heightmap = editor.worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"] # type: ignore

#  y = Foundation height
y = heightmap[1, 1] + 10 # + 3 is temporary while i do blueprints

# x & z coordinates to build the house
houseX = buildArea.offset.x + 1
houseZ = buildArea.offset.z + 1

height = 5

# region LIVINGROOM
# Coordinates
# Width
lRoomX1 = houseX + 25 # always 25 blocks from edge
lRoomX2 = lRoomX1 + 9#randint(7, 10)

#Depth
lRoomZ1 = houseZ # + 10 # always 10 blocks from edge
lRoomZ2 = lRoomZ1 + 16#randint(13, 16)

# Livingroom Palette
livingRoomWall = Block("white_concrete")
livingRoomFloor = Block("white_wool")

# Livingroom Wall
placeCuboidHollow(editor, (lRoomX1, y, lRoomZ1), (lRoomX2, y + height, lRoomZ2), livingRoomWall)

# Livingroom Floor
placeCuboidHollow(editor, (lRoomX1, y, lRoomZ1), (lRoomX2, y, lRoomZ2), livingRoomFloor)
# endregion

# region GARAGE
# Coordinates
# Width
garageWidth = 9#choice([7, 9])
garageDoorWidth = math.floor((garageWidth - 2) / 2)
garageX1 = lRoomX2 + 1
garageX2 = garageX1 + garageWidth
garageDoorsOpen = 0 #randint(0, 1)

# Depth
garageZ1 = int((lRoomZ1 * .7 + lRoomZ2 * 0.3))
garageZ2 = lRoomZ2

#Garage Palette
garageWall = Block("gray_concrete")
garageFloor = Block("gray_wool")
garageDoor = Block("pale_oak_door", {"facing": "west", "hinge": "left"})

# Garage Wall + Door
placeCuboidHollow(editor, (garageX1, y, garageZ1), (garageX2, y + height, garageZ2), garageWall)
editor.placeBlock((garageX1, y+1, garageZ2 - 2), garageDoor)
garageLeftX1 = garageX2 - 1
garageRightX1 = garageX1 + 1

if garageDoorsOpen == 0:
    garageBigDoors = Block("iron_trapdoor", {"facing": "south", "half": "bottom", "open": "true"})
    garageLeftX2 = garageLeftX1 - garageDoorWidth
    garageRightX2 = garageRightX1 + garageDoorWidth

    # Left Big Door
    placeCuboidHollow(editor, (garageLeftX1, y + 1, garageZ1),
                    (garageLeftX2, y + height - 1, garageZ1), garageBigDoors)

    # Right Big Door
    placeCuboidHollow(editor, (garageRightX1, y + 1, garageZ1),
                    (garageRightX2, y + height - 1, garageZ1), garageBigDoors)

else:
    garageLeftDoors = Block("iron_trapdoor", {"facing": "west", "half": "bottom", "open": "true"})
    garageRightDoors = Block("iron_trapdoor", {"facing": "east", "half": "bottom", "open": "true"})
    garageLeftZ2 = garageZ1 - garageDoorWidth - 1
    garageLeftZ1 = garageZ1
    
    garageRightZ2 = garageZ1 - garageDoorWidth - 1
    garageRightZ1 = garageZ1

    # Left Big Door
    placeCuboidHollow(editor, (garageLeftX1, y + 1, garageLeftZ1),
                    (garageLeftX1, y + height - 1, garageLeftZ2), garageLeftDoors)

    # Right Big Door
    placeCuboidHollow(editor, (garageRightX1, y + 1, garageRightZ1),
                    (garageRightX1, y + height - 1, garageRightZ2), garageRightDoors)
    
    # Clear the space between the open doors
    placeCuboidHollow(editor, (garageLeftX1, y + 1, garageZ1),
                    (garageRightX1, y + height - 1, garageZ1), Block("air"))
    
# Garage Floor
placeCuboidHollow(editor, (garageX1, y, garageZ1), (garageX2, y, garageZ2), garageFloor)
# endregion

# region HALLWAY
# Coordinates
# Width --- Should be dependent on the size of the rooms!
# Or actually; the rooms should be dependent on the size of the hallways.
hallwayWidth  = 3
hallwayLength = 18 # randint(10, 18) # randint(10, 20) # till 18---
hallwayX1 = lRoomX1
hallwayX2 = hallwayX1 - hallwayLength # randint(6, 8)

#Depth
hallwayZ1 = (lRoomZ1 + lRoomZ2) / 2 - 2
hallwayZ2 = hallwayZ1 + 3

# Hallway Palette
hallwayWall = Block("blue_concrete")
hallwayFloor = Block("blue_wool")

# Hallway Wall 
placeCuboidHollow(editor, (hallwayX1, y, hallwayZ1), (hallwayX2, y + height, hallwayZ2), hallwayWall) # type: ignore

# Hallway Floor
placeCuboidHollow(editor, (hallwayX1, y, hallwayZ1), (hallwayX2, y, hallwayZ2), hallwayFloor) # type: ignore

# Opens up hallway
placeCuboid(editor, (hallwayX1, y + 1, hallwayZ1), (hallwayX1, y + height - 1, hallwayZ2), Block("air")) # type: ignore

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

placeCuboidHollow(editor, (bedroom1X1, y, bedroom1Z1), (bedroom1X2, y + height, bedroom1Z2), bedroom1Wall) # type: ignore
placeCuboidHollow(editor, (bedroom1X1, y, bedroom1Z1), (bedroom1X2, y, bedroom1Z2), bedroom1Floor) # type: ignore
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

placeCuboidHollow(editor, (bedroom2X1, y, bedroom2Z1), (bedroom2X2, y + height, bedroom2Z2), bedroom2Wall) # type: ignore
placeCuboidHollow(editor, (bedroom2X1, y, bedroom2Z1), (bedroom2X2, y, bedroom2Z2), bedroom2Floor) # type: ignore
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

    placeCuboidHollow(editor, (bedroom3X1, y, bedroom3Z1), (bedroom3X2, y + height, bedroom3Z2), bedroom3Wall) # type: ignore
    placeCuboidHollow(editor, (bedroom3X1, y, bedroom3Z1), (bedroom3X2, y, bedroom3Z2), bedroom3Floor) # type: ignore
    # endregion


print("Bedroom Count:", bedroomCount)

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

placeCuboidHollow(editor, (kitchenX1, y, kitchenZ1), (kitchenX2, y + height, kitchenZ2), kitchenWall) # type: ignore
placeCuboidHollow(editor, (kitchenX1, y, kitchenZ1), (kitchenX2, y, kitchenZ2), kitchenFloor) # type: ignore
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

placeCuboidHollow(editor, (bathroomX1, y, bathroomZ1), (bathroomX2, y + height, bathroomZ2), bathroomWall) # type: ignore
placeCuboidHollow(editor, (bathroomX1, y, bathroomZ1), (bathroomX2, y, bathroomZ2), bathroomFloor) # type: ignore

# endregion

# Removes top layer so I can see blueprint
placeCuboid(editor, (houseX, y + height, houseZ), (houseX + 100, y + height, houseZ + 100), Block("air"))

# Add double doors
editor.placeBlock((lRoomX1+2, y+1, lRoomZ1), Block("oak_door", {"facing": "south", "hinge": "right"}))
editor.placeBlock((lRoomX1+3, y+1, lRoomZ1), Block("oak_door", {"facing": "south", "hinge": "left"}))