#!/usr/bin/python3
"""
Generates mazes.
"""

import sys
import argparse
import subprocess

import mazelib


def get_special_char(capname):
    # See manpage for "terminfo" for capname values.
    return subprocess.check_output(["tput", capname]).decode()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("width", nargs="?", type=int, default=50,
            help="Width of the maze.")
    parser.add_argument("height", nargs="?", type=int, default=30,
            help="Height of the maze.")
    parser.add_argument("--algorithm", "-a", default="backtrack",
            choices=mazelib.generators.keys(),
            help="Maze generation algorithm to use.")
    parser.add_argument("--progress", "-p", default=False, action="store_true",
            help="Prints the maze as it is being generated. "
            "Not all generation algorithms support this")
    parser.add_argument("--skip", "-s", default=0, type=int,
            help="When using --progress, skip this many intermediate steps "
            "before printing again.")
    parser.add_argument("--grid", "-g", default="rect",
            choices=mazelib.maze_types.keys(),
            help="Maze grid type to use.")
    args = parser.parse_args()

    maze_cls = mazelib.maze_types[args.grid]

    if args.progress:
        clear_chr = get_special_char("clear")
        lineup_chr = get_special_char("cuu1")  # Moves cursor 1 line up

        m = maze_cls(args.width, args.height)
        cls = mazelib.generators[args.algorithm]
        gen = cls(m)
        print(clear_chr)
        for i, m in enumerate(gen.iter_steps()):
            if i % (args.skip+1) == 0:
                s = m.to_str()
                print(lineup_chr*(s.count("\n")+1), end="")
                print(s)

        print(clear_chr)
        print(m.to_str())

    else:
        m = maze_cls(args.width, args.height)
        cls = mazelib.generators[args.algorithm]
        gen = cls(m)
        m = gen.generate()
        print(m.to_str())


if __name__ == "__main__":
    main()
