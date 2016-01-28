
import sys
if sys.version_info < (3, 2):
    raise RuntimeError("Python version 3.2 or greater is required")


from mazelib.maze import Maze, RectMaze, HexMaze
from mazelib import generate

##### Generators #####
generators = {}
def register_gen_class(cls):
    assert cls.name != None
    assert cls.name not in generators
    generators[cls.name] = cls

def register_gen_classes(classes):
    for cls in classes:
        register_gen_class(cls)

register_gen_classes([
    generate.Backtrack,
    generate.BacktrackRecursive,
    generate.Kruskal,
])

##### Maze Types #####
maze_types = {}
def register_maze_type(cls):
    assert cls.name != None
    assert cls.name not in maze_types
    maze_types[cls.name] = cls

def register_maze_types(classes):
    for cls in classes:
        register_maze_type(cls)

register_maze_types([
    RectMaze,
    HexMaze,
])
