
import numpy


class Maze():
    default_enter_side = None
    default_exit_side = None

    def opposite_dir(self, direction):
        raise NotImplementedError()

    def to_str(self):
        raise NotImplementedError()

    def to_img(self):
        raise NotImplementedError()

    def __getitem__(self, cell_id):
        return self.cell_get(cell_id)

    ########## Sides ##########
    side_ids = ()

    def sides_get_all(self):
        return map(lambda s: Side(s, self), self.side_ids)

    def side_get(self, side_id):
        assert side_id in self.side_ids
        return Side(side_id, self)

    def side_get_walls(self, side_id):
        raise NotImplementedError()

    def side_get_cells(self, side_id):
        return map(lambda x: x.c1, self.side_get_walls(side_id))

    ########## Cells ##########

    def cells_get_all(self):
        raise NotImplementedError()

    def cell_get(self, cell_id):
        return Cell(cell_id, self)

    def cell_get_walls(self, cell_id):
        raise NotImplementedError()

    def cell_get_neighbor(self, cell_id, direction):
        raise NotImplementedError()

    def cell_is_on_side(self, cell_id, side_id):
        return cell_id in map(lambda x: x.cell_id, self.side_get_cells(side_id))

    def cell_get_side_wall(self, cell_id, side_id):
        for wall in self.side_get_walls(side_id):
            if wall.c1.cell_id == cell_id:
                return wall
        return None

    ########## Walls ##########

    def walls_get_all(self):
        raise NotImplementedError()

    def wall_get(self, cell_id, direction):
        #TODO: Implement this generally.
        raise NotImplementedError()

    def wall_opposite_side(self, cell_id, direction):
        opposite = self.cell_get_neighbor(cell_id, direction)
        if opposite:
            opposite_id = opposite.cell_id
        else:
            opposite_id = None
        return (
            opposite_id,
            self.opposite_dir(direction)
        )

    def wall_set(self, cell_id, direction, set_to=True):
        raise NotImplementedError()

    def wall_remove(self, cell_id, direction):
        self.wall_set(cell_id, direction, set_to=False)


#################### Helper Classes ####################

class Side():

    def __init__(self, side_id, maze):
        assert side_id is not None

        self.side_id = side_id
        self.maze = maze

    @property
    def walls(self):
        return self.maze.side_get_walls(self.side_id)

    @property
    def cells(self):
        return self.maze.side_get_cells(self.side_id)


class Cell():

    def __init__(self, cell_id, maze):
        assert cell_id is not None
        self.cell_id = cell_id
        self.maze = maze

    def __eq__(self, other):
        return other.maze == self.maze and other.cell_id == self.cell_id

    def __getitem__(self, direction):
        return self.wall_get(direction)

    def __setitem__(self, direction, value):
        self.wall_set(direction, value)

    @property
    def walls(self):
        return self.maze.cell_get_walls(self.cell_id)

    @property
    def interior_walls(self):
        return filter(lambda w: w.interior, self.walls)

    def wall_set(self, direction, set_to=True):
        self.maze.wall_set(self.cell_id, direction, set_to)

    def wall_remove(self, direction):
        self.maze.wall_set(self.cell_id, direction, False)

    def wall_get(self, direction):
        return self.maze.wall_get(self.cell_id, direction)

    def is_on_side(self, side):
        if isinstance(side, Side):
            side = side.side_id
        return self.maze.cell_is_on_side(self.cell_id, side)

    def get_side_wall(self, side):
        if isinstance(side, Side):
            side = side.side_id
        return self.maze.cell_get_side_wall(self.cell_id, side)


class Wall():

    def __init__(self, cell_id, direction, maze):
        assert cell_id is not None
        assert direction is not None

        self.c1_id = cell_id
        self.c1 = Cell(cell_id, maze)
        self.d1 = direction

        self.c2_id, self.d2 = maze.wall_opposite_side(cell_id, direction)
        self.c2 = Cell(self.c2_id, maze) if self.c2_id else None

        self.maze = maze

    def __bool__(self):
        return self.get()

    def get(self):
        return self.maze.wall_get(self.c1_id, self.d1)

    def set(self, set_to=True):
        self.maze.wall_set(self.c1_id, self.d1, set_to)

    def remove(self):
        self.maze.wall_set(self.c1_id, self.d1, False)

    @property
    def exterior(self):
        return self.c2_id is None

    @property
    def interior(self):
        return self.c2_id is not None


#################### RectMaze ####################

class RectMaze(Maze):
    N, S, E, W = (1, 2, 4, 8)  # North, South, East West
    OPPOSITE_DIR = {
        N: S,
        S: N,
        E: W,
        W: E,
    }
    DELTAS = {
        N: ( 0, -1),
        S: ( 0,  1),
        E: ( 1,  0),
        W: (-1,  0),
    }

    WALL_CHARS = {
        0      : ' ',
        N      : '╵',
        S    : '╷',
        N|S    : '│',
            E  : '╶',
        N  |E  : '╰',
        S|E  : '╭',
        N|S|E  : '├',
            W: '╴',
        N    |W: '╯',
        S  |W: '╮',
        N|S  |W: '┤',
            E|W: '─',
        N  |E|W: '┴',
        S|E|W: '┬',
        N|S|E|W: '┼',
    }

    side_ids = set((N, S, E, W))
    default_enter_side = N
    default_exit_side = S

    def __init__(self, width, height):
        self.width = width
        self.height = height

        default_cell = self.N | self.S | self.E | self.W
        self._cells = numpy.array(
            [[default_cell for y in range(self.height)]
                           for x in range(self.width)],
            dtype=numpy.uint8
        )

    def opposite_dir(self, direction):
        return self.OPPOSITE_DIR[direction]

    def in_bounds(self, x, y):
        return x>=0 and y>=0 and x<self.width and y<self.height

    def to_str(self):
        s = []
        for y in range(-1, self.height):
            for x in range(-1, self.width):

                #TODO: Probably unnessesary to check all 4 surrounding cells,
                #      but I wanted to be careful around the corners/edges of
                #      the maze.
                a = 0
                if self.in_bounds(x, y):
                    if self._cells[x,y] & self.E: a |= self.N
                    if self._cells[x,y] & self.S: a |= self.W
                if self.in_bounds(x+1, y):
                    if self._cells[x+1,y] & self.W: a |= self.N
                    if self._cells[x+1,y] & self.S: a |= self.E
                if self.in_bounds(x, y+1):
                    if self._cells[x,y+1] & self.E: a |= self.S
                    if self._cells[x,y+1] & self.N: a |= self.W
                if self.in_bounds(x+1, y+1):
                    if self._cells[x+1,y+1] & self.W: a |= self.S
                    if self._cells[x+1,y+1] & self.N: a |= self.E

                s.append(self.WALL_CHARS[a])
            s.append("\n")
        return ''.join(s[:-1])

    ########## Sides ##########

    def side_get_walls(self, side_id):
        assert side_id in self.side_ids
        if side_id in (self.N, self.S):
            y = 0 if side_id == self.N else self.height-1
            for x in range(self.width):
                yield Wall((x, y), side_id, self)
        else:
            x = 0 if side_id == self.W else self.width-1
            for y in range(self.height):
                yield Wall((x, y), side_id, self)

    ########## Cells ##########

    def cells_get_all(self):
        for y in range(self.height):
            for x in range(self.width):
                yield Cell((x, y), self)

    def cell_get_walls(self, cell_id):
        for d in self.side_ids:
            yield Wall(cell_id, d, self)

    def cell_get_neighbor(self, cell_id, direction):
        x, y = cell_id
        dx, dy = self.DELTAS[direction]
        if not self.in_bounds(x+dx, y+dy):
            return None
        else:
            return Cell((x+dx, y+dy), self)

    ########## Walls ##########

    def walls_get_all(self):
        for x in range(self.width-1):
            for y in range(self.height-1):
                yield Wall((x, y), self.E, self)
                yield Wall((x, y), self.S, self)

        for x in range(self.width-1):
            yield Wall((x, self.height-1), self.E, self)

        for y in range(self.height-1):
            yield Wall((self.width-1, y), self.S, self)

    def wall_get(self, cell_id, direction):
        return self._cells[cell_id] & direction > 0

    def wall_set(self, cell_id, direction, set_to=True):
        if set_to is True:
            self._cells[cell_id] |= direction
        else:
            self._cells[cell_id] &= ~direction & 0xf

        new_coordinates = tuple(numpy.array(cell_id) + self.DELTAS[direction])
        if self.in_bounds(*new_coordinates):
            if set_to is True:
                self._cells[new_coordinates] |= self.opposite_dir(direction)
            else:
                self._cells[new_coordinates] &= ~self.opposite_dir(direction) & 0xf


#################### HexMaze ####################

class HexMaze(Maze):

    N, S, NE, NW, SE, SW = (1, 2, 4, 8, 16, 32)
    E, W = (64, 128)  # Used for sides, not wall directions
    DIRECTIONS = set((N, S, NE, NW, SE, SW))
    OPPOSITE_DIR = {
        N: S,
        S: N,
        E: W,
        W: E,
        NE: SW,
        SW: NE,
        NW: SE,
        SE: NW,
    }

    side_ids = set((N, S, E, W))
    default_enter_side = N
    default_exit_side = S

    def __init__(self, width, height):
        assert height > 1
        self.width = width
        self.height = height

        # Coordinate system: x,y
        #  ___     ___     ___
        # ╱0,0╲___╱1,0╲___╱2,0╲___
        # ╲___╱0,1╲___╱1,1╲___╱2,1╲  ...
        # ╱0,2╲___╱1,2╲___╱2,2╲___╱
        # ╲___╱   ╲___╱   ╲___╱
        #            ...
        default_cell = self.N | self.S | self.NE | self.NW | self.SE | self.SW
        self._cells = numpy.array(
            [[default_cell for y in range(self.height)]
                           for x in range(self.width)],
            dtype=numpy.uint8
        )

    def opposite_dir(self, direction):
        return self.OPPOSITE_DIR[direction]

    def in_bounds(self, x, y):
        return x>=0 and y>=0 and x<self.width and y<self.height

    def get_direction_delta(self, direction, y):
        if   direction == self.N:  return (0, -2)
        elif direction == self.S:  return (0, 2)
        elif direction == self.NE: return (1 if y&1 else 0, -1)
        elif direction == self.SW: return (0 if y&1 else -1, 1)
        elif direction == self.NW: return (0 if y&1 else -1, -1)
        elif direction == self.SE: return (1 if y&1 else 0, 1)

    def to_str(self):
        s = []  # Result string

        # Print wall
        # Shortcut for conditional appending to the result.
        # If Wall((x, y), direction) is set, add if_set to the result
        # string s, otherwise add if_unset.
        def p(x, y, direction, if_set, if_unset=""):
            assert self.in_bounds(x, y)
            if self._cells[x, y] & direction:
                s.append(if_set)
            else:
                s.append(if_unset)

        # Shortcut vars
        w, h = self.width, self.height
        N, NW, NE = self.N, self.NW, self.NE
        S, SW, SE = self.S, self.SW, self.SE

        # First Row
        s.append(" ")
        for x in range(w):
            p(x, 0, N, "__    ", "      ")
        s.append("\n")

        for y in range(0, h, 2):

            # Top of even rows
            for x in range(w):
                p(x, y, NW, "╱  ", "   ")
                p(x, y, NE, "╲", " ")
                if y > 0:
                    p(x, y-1, S, "__", "  ")
                else:
                    p(x, y+1, N, "__", "  ")
            if y > 0:
                p(w-1, y-1, SE, "╱")
            s.append("\n")

            # Bottom of even rows
            for x in range(w):
                p(x, y, SW, "╲", " ")
                p(x, y, S, "__", "  ")
                p(x, y, SE, "╱", " ")
                s.append("  ")
            if y+1 < h:
                p(x, y+1, NE, "╲")
            s.append("\n")

        # Last row
        if h&1 == 0:  # Num rows is even
            s.append(" ")
            for x in range(w):
                s.append("  ")
                p(x, h-1, SW, "╲", " ")
                p(x, h-1, S, "__", "  ")
                p(x, h-1, SE, "╱", " ")
            s.append("\n")

        return ''.join(s[:-1])

    ########## Sides ##########

    def side_get_walls(self, side_id):
        assert side_id in self.side_ids

        if side_id == self.N:
            for x in range(self.width):
                yield Wall((x, 0), self.NW, self)
                yield Wall((x, 0), self.N, self)
                yield Wall((x, 0), self.NE, self)
                yield Wall((x, 1), self.N, self)

        elif side_id == self.S:

            for x in range(self.width):
                yield Wall((x, self.height-1), self.SW, self)
                yield Wall((x, self.height-1), self.S, self)
                yield Wall((x, self.height-1), self.SE, self)
                yield Wall((x, self.height-2), self.S, self)

        elif side_id == self.W:

            for y in range(0, self.height, 2):
                yield Wall((0, y), self.NW, self)
                yield Wall((0, y), self.SW, self)

        elif side_id == self.E:

            for y in range(1, self.height, 2):
                yield Wall((self.width-1, y), self.NE, self)
                yield Wall((self.width-1, y), self.SE, self)

    ########## Cells ##########

    def cells_get_all(self):
        for y in range(self.height):
            for x in range(self.width):
                yield Cell((x, y), self)

    def cell_get_walls(self, cell_id):
        for d in self.DIRECTIONS:
            yield Wall(cell_id, d, self)

    def cell_get_neighbor(self, cell_id, direction):
        x, y = cell_id
        dx, dy = self.get_direction_delta(direction, y)
        if not self.in_bounds(x+dx, y+dy):
            return None
        else:
            return Cell((x+dx, y+dy), self)

    ########## Walls ##########

    def walls_get_all(self):

        # NW, N & NE for every cell
        for x in range(self.width):
            for y in range(self.height):
                yield Wall((x, y), self.NW, self)
                yield Wall((x, y), self.N, self)
                yield Wall((x, y), self.NE, self)

        # Remainder of left & right side
        for y in range(0, self.height-1, 2):
            yield Wall((0, y), self.SW, self)
        for y in range(1, self.height-1, 2):
            yield Wall((self.width-1, y), self.SE, self)

        # Bottom wall
        yield from self.side_get_walls(self.S)

    def wall_get(self, cell_id, direction):
        return self._cells[cell_id] & direction > 0

    def wall_set(self, c1_id, d1, set_to=True):
        c2 = self.cell_get_neighbor(c1_id, d1)
        c2_id = c2.cell_id if c2 else None
        d2 = self.opposite_dir(d1)

        if set_to is True:
            self._cells[c1_id] |= d1
            if c2:
                self._cells[c2_id] |= d2
        else:
            self._cells[c1_id] &= ~d1 & 0x3f
            if c2:
                self._cells[c2_id] &= ~d2 & 0x3f
