
import random
import collections

from mazelib import Maze


class MazeGen():
    name = None

    def __init__(self, maze):
        self.m = maze

    def init(self):
        pass

    def step(self):
        pass

    def is_finished(self):
        raise NotImplementedError()

    def finish(self):
        return self.m

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


class Backtrack(MazeGen):
    """
        http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking
    """
    name = "backtrack"

    def init(self):

        # Entrance fixed here to be random
        enter_wall = random.choice(list(
            self.m.side_get(self.m.default_enter_side).walls
        ))
        enter_wall.remove()
        enter_cell = enter_wall.c1

        # Exit chosen random for now, but will be changed later to be the
        # furthest possible from the entrance. Only at the end will we remove
        # this wall, since these will change during generation.
        self.exit_cell = random.choice(list(
            self.m.side_get(self.m.default_exit_side).cells
        ))
        self.exit_dist = 0  # Distance between entrance and exit

        self.stack = [enter_cell]
        self.visited = set(enter_cell.cell_id)

    def step(self):
        cell = self.stack[-1]

        # Move exit cell if this is further away from the entrance than the
        # current one.
        if cell.is_on_side(self.m.default_exit_side) and len(self.stack) > self.exit_dist:
            self.exit_dist = len(self.stack)
            self.exit_cell = cell

        walls = list(cell.interior_walls)
        random.shuffle(walls)
        neighbor_found = False
        for wall in walls:
            other_cell = wall.c2
            if other_cell.cell_id not in self.visited:
                wall.remove()
                self.stack.append(other_cell)
                self.visited.add(other_cell.cell_id)
                neighbor_found = True
                break
        if not neighbor_found:
            self.stack.pop()

        return self.m

    def finish(self):
        self.exit_cell.get_side_wall(self.m.default_exit_side).remove()
        return self.m

    def is_finished(self):
        return len(self.stack) == 0


class BacktrackRecursive(MazeGen):
    """
        http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking
    """
    name = "backtrack_recursive"

    def generate(self):

        enter_wall = random.choice(list(
            self.m.side_get(self.m.default_enter_side).walls
        ))
        enter_wall.remove()

        exit_wall = random.choice(list(
            self.m.side_get(self.m.default_exit_side).walls
        ))
        exit_wall.remove()

        visited = set()
        def recurse(cell):
            visited.add(cell.cell_id)
            walls = list(cell.interior_walls)
            random.shuffle(walls)
            for wall in walls:
                other_cell = wall.c2
                if other_cell.cell_id not in visited:
                    wall.remove()
                    recurse(other_cell)

        recurse(enter_wall.c1)

        return self.m


class Kruskal(MazeGen):
    """
        http://weblog.jamisbuck.org/2011/1/3/maze-generation-kruskal-s-algorithm
    """
    name = "kruskal"

    def init(self):
        self.candidate_walls = filter(lambda w: w.interior, self.m.walls_get_all())
        self.candidate_walls = list(self.candidate_walls)
        random.shuffle(self.candidate_walls)
        self.labels = {}  # Maps cell ids to labels

        # Remove random entrance wall
        enter_wall = random.choice(list(
            self.m.side_get(self.m.default_enter_side).walls
        ))
        enter_wall.remove()

        # Remove random exit wall
        exit_wall = random.choice(list(
            self.m.side_get(self.m.default_exit_side).walls
        ))
        exit_wall.remove()

    def step(self):
        w = self.candidate_walls.pop()
        label1 = self.labels.get(w.c1.cell_id, w.c1.cell_id)
        label2 = self.labels.get(w.c2.cell_id, w.c2.cell_id)
        if label1 != label2:
            w.remove()

            # Set c1's label to c2's
            self.labels[w.c1.cell_id] = label2
            self.labels[w.c2.cell_id] = label2
            for cell_id, label in self.labels.items():
                if label == label1:
                    self.labels[cell_id] = label2

        return self.m

    def is_finished(self):
        return len(self.candidate_walls) == 0
