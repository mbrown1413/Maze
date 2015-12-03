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
    parser.add_argument("--algorithm", "--alg", "-a", default="backtracking",
            choices=mazelib.generators.keys(),
            help='Maze generation algorithm to use. One of: '
            '{}'.format(list(mazelib.generators.keys())))
    parser.add_argument("--progress", "-p", default=False, action="store_true",
            help="Prints the maze as it is being generated. "
            "Not all generation algorithms support this")
    parser.add_argument("--skip", "-s", default=0, type=int,
            help="When using --progress, skip this many intermediate steps "
            "before printing again.")
    args = parser.parse_args()

    if args.progress:
        clear_chr = get_special_char("clear")
        lineup_chr = get_special_char("cuu1")  # Moves cursor 1 line up

        cls = mazelib.generators[args.algorithm]
        g = cls(args.width, args.height)
        print(clear_chr)
        for i, m in enumerate(g.iter_steps()):
            if i % (args.skip+1) == 0:
                print(lineup_chr*(args.height+1) + m.to_str())
        if i % (args.skip+1) != 0:
            print(lineup_chr*(args.height+1) + m.to_str())

    else:
        m = mazelib.gen(args.algorithm, args.width, args.height)
        print(m.to_str())


if __name__ == "__main__":
    main()
