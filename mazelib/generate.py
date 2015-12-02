
import random
import collections

from mazelib import Maze, N, E, S, W, DIRECTIONS, DELTAS


class MazeGen():
    name = None

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def init(self):
        pass

    def step(self):
        pass

    def is_finished(self):
        raise NotImplementedError()

    def finish(self):
        raise NotImplementedError()

    def generate(self):
        self.init()
        while not self.is_finished():
            self.step()
        return self.finish()

    def iter_steps(self):
        self.init()
        while not self.is_finished():
            yield self.step()
        yield self.finish()

    def in_bounds(self, x, y):
        return x>=0 and y>=0 and x<self.width and y<self.height


class Backtracking(MazeGen):
    """
        http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking
    """
    name = "backtracking"

    def init(self):
        self.m = Maze(self.width, self.height)

        self.enter_x = 0
        self.exit_x = random.randrange(self.width)
        self.m[self.enter_x,0].remove(N)

        self.longest_bot_path = 0
        self.stack = [(self.enter_x, 0)]
        self.visited = set(self.stack)

    def step(self):
        x, y = self.stack[-1]

        if y == self.height-1 and len(self.stack) > self.longest_bot_path:
            self.longest_bot_path = len(self.stack)
            self.exit_x = x

        ds = list(DIRECTIONS)
        random.shuffle(ds)
        neighbor_found = False
        for d in ds:
            nx = x + DELTAS[d][0]
            ny = y + DELTAS[d][1]
            if self.in_bounds(nx, ny) and (nx, ny) not in self.visited:
                self.m[x,y].remove(d)
                self.stack.append((nx, ny))
                self.visited.add((nx, ny))
                neighbor_found = True
                break
        if not neighbor_found:
            self.stack.pop()

        return self.m

    def finish(self):
        self.m[self.exit_x,self.height-1].remove(S)
        return self.m

    def is_finished(self):
        return len(self.stack) == 0


class BacktrackingRecursive(MazeGen):
    """
        http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking
    """
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


class Kruskal(MazeGen):
    """
        http://weblog.jamisbuck.org/2011/1/3/maze-generation-kruskal-s-algorithm
    """
    name = "kruskal"

    Wall = collections.namedtuple("Wall", "c1 d c2")

    def generate(self):
        m = Maze(self.width, self.height)

        candidate_walls = set(self.get_all_walls())
        labels = [[(x,y) for y in range(self.height)]
                         for x in range(self.width)]

        while candidate_walls:
            w = random.choice(list(candidate_walls))
            candidate_walls.remove(w)
            if labels[w.c1[0]][w.c1[1]] != labels[w.c2[0]][w.c2[1]]:
                m[w.c1].remove(w.d)
                c2_label = labels[w.c2[0]][w.c2[1]]
                self.chance_label(labels, w.c1, c2_label)

        #TODO: Better enter and exit
        enter_x = random.randrange(self.width)
        exit_x = random.randrange(self.width)
        m[enter_x,0].remove(N)
        m[exit_x,self.height-1].remove(S)

        return m

    def chance_label(self, labels, coordinates, new_label):
        x, y = coordinates
        old_label = labels[x][y]
        for x in range(self.width):
            for y in range(self.height):
                if labels[x][y] == old_label:
                    labels[x][y] = new_label

    def get_all_walls(self):
        for x in range(self.width-1):
            for y in range(self.height-1):
                yield self.Wall((x, y), E, (x+1, y))
                yield self.Wall((x, y), S, (x, y+1))

        for x in range(self.width-1):
            yield self.Wall((x, self.height-1), E, (x+1, self.height-1))

        for y in range(self.height-1):
            yield self.Wall((self.width-1, y), S, (self.width-1, y+1))
