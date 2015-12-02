
import sys
if sys.version_info < (3, 2):
    raise RuntimeError("Python version 3.2 or greater is required")


from mazelib.maze import Maze, Cell
from mazelib.maze import N, S, E, W, NORTH, SOUTH, EAST, WEST
from mazelib.maze import DIRECTIONS, OPPOSITE_DIRECTION, DELTAS

generators = {}
def register_gen_class(cls):
    assert cls.name != None
    assert cls.name not in generators
    generators[cls.name] = cls

def register_gen_classes(classes):
    for cls in classes:
        register_gen_class(cls)

def gen(alg_name, width, height, *args, **kwargs):
    cls = generators[alg_name]
    g = cls(width, height, *args, **kwargs)
    return g.generate()

from mazelib import generate
register_gen_classes([
    generate.Backtracking,
    generate.BacktrackingRecursive,
    generate.Kruskal,
])
