import fileinput
from functools import reduce
from typing import List


def process(forest: List, y_slope: int, x_slope: int) -> int:
    """
    Step through a 'forest' with slope x=x_slope, y=y_slope.
    The forest repeats itself, so when x is bigger than the length of
    a forest row, it can be wrapped to the start of the line.
    Returns the number of trees (#) found along the way.

    :param forest: list of forest row strings (e.g. .....#......#.........#..##.#..)
    :param y_slope: int
    :param x_slope:
    :return: number of trees passed
    """
    y_pos = 0
    x_pos = 0
    n_trees = 0
    for i, row in enumerate(forest):
        if y_pos == i:
            if x_pos >= len(row):
                x_pos -= len(row)
            if row[x_pos] == '#':
                n_trees += 1
            x_pos += x_slope
            y_pos += y_slope
    print('{} trees'.format(n_trees))
    return n_trees


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])

    # A list of slopes is processed, the result is multiplied together and printed
    outputs = []
    for slope in [(1, 3), (1, 1), (1, 5), (1, 7), (2, 1)]:
        outputs.append(process(lines, y_slope=slope[0], x_slope=slope[1]))
    print(reduce((lambda x, y: x * y), outputs))
