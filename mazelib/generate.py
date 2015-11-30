
import random

from mazelib import Maze, N, S, DIRECTIONS, DELTAS


class MazeGen():
    name = None

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def generate(self):
        raise NotImplementedError()


class Backtracking(MazeGen):
    name = "backtracking"

    def generate(self):
        m = Maze(self.width, self.height)

        #enter_x = random.randrange(self.width)
        enter_x = 0
        exit_x = random.randrange(self.width)
        m[enter_x,0].remove(N)

        longest_bot_path = 0
        stack = [(enter_x, 0)]
        visited = set(stack)
        while stack:
            x, y = stack[-1]
            #print(m.to_str())
            #import time; time.sleep(0.01)

            if y == self.height-1 and len(stack) > longest_bot_path:
                longest_bot_path = len(stack)
                exit_x = x

            ds = list(DIRECTIONS)
            random.shuffle(ds)
            neighbor_found = False
            for d in ds:
                nx = x + DELTAS[d][0]
                ny = y + DELTAS[d][1]
                if m.in_bounds(nx, ny) and (nx, ny) not in visited:
                    m[x,y].remove(d)
                    stack.append((nx, ny))
                    visited.add((nx, ny))
                    neighbor_found = True
                    break
            if not neighbor_found:
                stack.pop()

        m[exit_x,self.height-1].remove(S)
        return m


class BacktrackingRecursive(MazeGen):
    name = "backtracking_recursive"

    def generate(self):
        m = Maze(self.width, self.height)

        enter_x = random.randrange(self.width)
        exit_x = random.randrange(self.width)
        m[enter_x,0].remove(N)
        m[exit_x,self.height-1].remove(S)

        visited = set()
        def recurse(x, y):
            ds = list(DIRECTIONS)
            visited.add((x, y))
            random.shuffle(ds)
            for d in ds:
                nx = x + DELTAS[d][0]
                ny = y + DELTAS[d][1]
                if m.in_bounds(nx, ny) and (nx, ny) not in visited:
                    m[x,y].remove(d)
                    recurse(nx, ny)

        recurse(enter_x, 0)

        return m
