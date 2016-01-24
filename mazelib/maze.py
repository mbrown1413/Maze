
class Maze():

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
        return map(Side, self.side_ids)

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

import numpy

NORTH = N = 1
SOUTH = S = 2
EAST = E = 4
WEST = W = 8
DELTAS = {
    N: ( 0, -1),
    S: ( 0,  1),
    E: ( 1,  0),
    W: (-1,  0),
}
OPPOSITE_DIR = {
    N: S,
    S: N,
    E: W,
    W: E,
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

class RectMaze(Maze):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._cells = numpy.array(
            [[N | S | E | W for y in range(self.height)]
                            for x in range(self.width)],
            dtype=numpy.uint8
        )

    def opposite_dir(self, direction):
        return OPPOSITE_DIR[direction]

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
                    if self._cells[x,y] & E: a |= N
                    if self._cells[x,y] & S: a |= W
                if self.in_bounds(x+1, y):
                    if self._cells[x+1,y] & W: a |= N
                    if self._cells[x+1,y] & S: a |= E
                if self.in_bounds(x, y+1):
                    if self._cells[x,y+1] & E: a |= S
                    if self._cells[x,y+1] & N: a |= W
                if self.in_bounds(x+1, y+1):
                    if self._cells[x+1,y+1] & W: a |= S
                    if self._cells[x+1,y+1] & N: a |= E

                s.append(WALL_CHARS[a])
            s.append("\n")
        return ''.join(s[:-1])

    ########## Sides ##########
    side_ids = set((N, S, E, W))

    def side_get_walls(self, side_id):
        assert side_id in self.side_ids
        if side_id in (N, S):
            y = 0 if side_id == N else self.height-1
            for x in range(self.width):
                yield Wall((x, y), side_id, self)
        else:
            x = 0 if side_id == W else self.width-1
            for y in range(self.height):
                yield Wall((x, y), side_id, self)

    ########## Cells ##########

    def cells_get_all(self):
        for y in range(self.height):
            for x in range(self.width):
                yield Cell((x, y), self)

    def cell_get_walls(self, cell_id):
        for d in (N, S, E, W):
            yield Wall(cell_id, d, self)

    def cell_get_neighbor(self, cell_id, direction):
        x, y = cell_id
        dx, dy = DELTAS[direction]
        if not self.in_bounds(x+dx, y+dy):
            return None
        else:
            return Cell((x+dx, y+dy), self)

    ########## Walls ##########

    def walls_get_all(self):
        for x in range(self.width-1):
            for y in range(self.height-1):
                yield Wall((x, y), E, self)
                yield Wall((x, y), S, self)

        for x in range(self.width-1):
            yield Wall((x, self.height-1), E, self)

        for y in range(self.height-1):
            yield Wall((self.width-1, y), S, self)

    def wall_get(self, cell_id, direction):
        return self._cells[cell_id] & direction > 0

    def wall_set(self, cell_id, direction, set_to=True):
        if set_to is True:
            self._cells[cell_id] |= direction
        else:
            self._cells[cell_id] &= ~direction & 0xf

        new_coordinates = tuple(numpy.array(cell_id) + DELTAS[direction])
        if self.in_bounds(*new_coordinates):
            if set_to is True:
                self._cells[new_coordinates] |= self.opposite_dir(direction)
            else:
                self._cells[new_coordinates] &= ~self.opposite_dir(direction) & 0xf
