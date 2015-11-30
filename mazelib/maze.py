
import numpy


NORTH = N = 1
SOUTH = S = 2
EAST = E = 4
WEST = W = 8
DIRECTIONS = (N, S, E, W)
DELTAS = {
    N: ( 0, -1),
    S: ( 0,  1),
    E: ( 1,  0),
    W: (-1,  0),
}
OPPOSITE_DIRECTION = {
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


class Maze():
    """
    m = Maze(5, 5)

    print(m[0, 0].n)

    m[0, 0].remove(W)
    m[0, 0].set(E)
    m[0, 0].n.remove()
    m[0, 0].n.set()
    m[0, 0].n.set(False)
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._cells = numpy.array(
            [[N | S | E | W for y in range(self.height)]
                            for x in range(self.width)],
            dtype=numpy.uint8
        )

    def __getitem__(self, coordinates):
        return Cell(coordinates, self)

    def set_wall(self, coordinates, direction, set_to=True):
        assert direction in DIRECTIONS

        if set_to is True:
            self._cells[coordinates] |= direction
        else:
            self._cells[coordinates] &= ~direction & 0xf

        new_coordinates = tuple(numpy.array(coordinates) + DELTAS[direction])
        if self.in_bounds(*new_coordinates):
            if set_to is True:
                self._cells[new_coordinates] |= OPPOSITE_DIRECTION[direction]
            else:
                self._cells[new_coordinates] &= ~OPPOSITE_DIRECTION[direction] & 0xf

    def del_wall(self, coordinates, direction):
        self.set_wall(coordinates, direction, False)

    def get_wall(self, coordinates, direction):
        assert direction in DIRECTIONS
        return self._cells[coordinates] & direction > 0

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
                    if self[x,y].get(E): a |= N
                    if self[x,y].get(S): a |= W
                if self.in_bounds(x+1, y):
                    if self[x+1,y].get(W): a |= N
                    if self[x+1,y].get(S): a |= E
                if self.in_bounds(x, y+1):
                    if self[x,y+1].get(E): a |= S
                    if self[x,y+1].get(N): a |= W
                if self.in_bounds(x+1, y+1):
                    if self[x+1,y+1].get(W): a |= S
                    if self[x+1,y+1].get(N): a |= E

                s.append(WALL_CHARS[a])
            s.append("\n")
        return ''.join(s[:-1])


class Cell():

    def __init__(self, coordinates, maze):
        self._coordinates = coordinates
        self._maze = maze

    def __eq__(self, other):
        return other._maze == self._maze and other._coordinates == self._coordinates

    def set(self, direction, set_to=True):
        self._maze.set_wall(self._coordinates, direction, set_to)

    def remove(self, direction):
        self._maze.set_wall(self._coordinates, direction, False)

    def get(self, direction):
        return self._maze.get_wall(self._coordinates, direction)
