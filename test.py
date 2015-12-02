#!/usr/bin/python3

import sys

import mazelib


def main():
    algorithm = "backtracking"
    width = 20
    height = 10
    if len(sys.argv) > 1:
        algorithm = sys.argv[1]
    if len(sys.argv) > 2:
        width = int(sys.argv[2])
    if len(sys.argv) > 3:
        height = int(sys.argv[3])
    if len(sys.argv) > 4:
        raise ValueError()

    cls = mazelib.generators[algorithm]
    g = cls(width, height)
    for m in g.iter_steps():
        print(m.to_str())


if __name__ == "__main__":
    main()
