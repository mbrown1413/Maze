
A simple maze generator framework.

## Usage

Requires:

  * Python 3
  * numpy

Generate a basic maze and specify width/height:

    $ python3 run.py 20 10
    ╭─┬──╴╶┬─┬───┬──────╮
    │╷│╶┬╮ │╷│╶╮╷╰╮╶┬╮╶╮│
    │╰┴╮╵╰┬┴┤├╴│╰╮╰╮╵╰╮╰┤
    │╷╷╰┬╮│╷│╵╶┼╴├╮╰┬╮├╴│
    ││╰╮╵│╵│╰──╯╭╯├╴│╵│╶┤
    │├╮├╴├─┴┬──┬╯╷│╶┴╮├╴│
    │││╰─╯╷╷╰╴╷│╭┤╰─╴││╷│
    │╵╰┬─╮│├─╴├╯│╰──┬╯│││
    ├┬╴│╷╰╯│╭─┤╭╯╷╭╮╰┬╯││
    │╵╶┤╰──┴╯╷╵╰─╯│╰╴╵╭╯│
    ╵╶─┴─────┴────┴───┴─╯

Use `--grid`/`-g` to change grid types:

    $ python3 run.py 5 10 --grid hex
      __    __    __    __    __
     ╱  ╲__╱  ╲__╱   __╱  ╲__╱  ╲__
     ╲  ╱     ╱   __   ╲     ╲__   ╲
     ╱   __╱   __╱   __   ╲__   ╲  ╱
     ╲  ╱  ╲__╱   __╱  ╲__╱  ╲  ╱  ╲
     ╱  ╲__    __   ╲  ╱   __   ╲  ╱
     ╲  ╱  ╲__   ╲  ╱  ╲  ╱  ╲__╱  ╲
     ╱     ╱  ╲__╱  ╲  ╱  ╲__    __╱
     ╲__╱   __    __╱  ╲__   ╲__   ╲
     ╱  ╲__╱  ╲__╱   __╱  ╲__      ╱
     ╲      __    __    __    __╱  ╲
        ╲__╱  ╲__╱  ╲__╱  ╲__╱  ╲__╱

Use `--algorithm`/`-a` to change generation algorithms:

    $ python3 run.py 10 20 --algorithm kruskal

Use `--progress`/`-p` to see the maze as it gets generated:

    $ python3 run.py 10 20 --progress

To see more options, use `--help`/`-h`

    $ python3 run.py --help


## For developers

Interesting files:

  * `mazelib/maze.py` - Maze representation.
  * `mazelib/generate.py` - Maze generation algorithms.
