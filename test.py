#!/usr/bin/python3

import sys
import subprocess

import mazelib


def get_special_char(capname):
    return subprocess.check_output(["tput", capname]).decode()

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

    clear_chr = get_special_char("clear")
    lineup_chr = get_special_char("cuu1")  # Moves cursor 1 line up

    cls = mazelib.generators[algorithm]
    g = cls(width, height)
    print(clear_chr)
    for m in g.iter_steps():
        print(lineup_chr*(height+1) + m.to_str())


if __name__ == "__main__":
    main()
