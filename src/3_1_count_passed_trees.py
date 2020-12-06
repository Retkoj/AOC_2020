import fileinput
from typing import List


def process(forest: List) -> None:
    """
    Step through a 'forest' with slope x=3, y=1. The forest repeats itself, so when x is bigger than the length of
    a forest row, it can be wrapped to the start of the line.
    Prints the number of trees (#) found along the way.

    :param forest: list of forest row strings (e.g. .....#......#.........#..##.#..)
    """
    x_pos = 0
    n_trees = 0
    for y_pos, row in enumerate(forest):
        if x_pos >= len(row):
            x_pos -= len(row)
        if row[x_pos] == '#':
            n_trees += 1
        x_pos += 3
    print('{} trees'.format(n_trees))


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    process(lines)
