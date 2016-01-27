
import sys
if sys.version_info < (3, 2):
    raise RuntimeError("Python version 3.2 or greater is required")


from mazelib.maze import Maze, RectMaze, HexMaze

generators = {}
def register_gen_class(cls):
    assert cls.name != None
    assert cls.name not in generators
    generators[cls.name] = cls

def register_gen_classes(classes):
    for cls in classes:
        register_gen_class(cls)

def gen(maze, alg_name, *args, **kwargs):
    cls = generators[alg_name]
    g = cls(maze, *args, **kwargs)
    return g.generate()

from mazelib import generate
register_gen_classes([
    generate.Backtrack,
    generate.BacktrackRecursive,
    generate.Kruskal,
])
