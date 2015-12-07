
A simple maze generator framework.

Requires:

  * Python 3
  * numpy

## Usage

Generate a basic maze:

    $ python3 run.py

Pass maze width and height as arguments:

    $ python3 run.py 10 20

Use `--algorithm` (or `-a`) to change generation algorithms:

    $ python3 run.py 10 20 -a kruskal

Use `--progress` (or `-p`) to see the maze as it gets generated:

    $ python3 run.py 10 20 -a kruskal -p

To see more options, use `--help`

    $ python3 run.py --help


## For developers

Interesting files:

  * `mazelib/maze.py` - Maze representation.
  * `mazelib/generate.py` - Maze generation algorithms.
