from gdpc import Editor, Block

editor = Editor(buffering=True)

buildArea = editor.getBuildArea()

y = 65

for x in range(buildArea.offset.x, buildArea.offset.x + 5):
    for z in range(buildArea.offset.z, buildArea.offset.z + 5):
        editor.placeBlock((x, y, z), Block("stone_bricks"))
