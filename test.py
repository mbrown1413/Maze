#!/usr/bin/python3

import sys

import mazelib


def main():
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

    m = mazelib.gen(algorithm, width, height)
    print(m.to_str())


if __name__ == "__main__":
    main()
