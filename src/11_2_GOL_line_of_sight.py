import fileinput

from GameOfLife import GameOfLife


def process(input_list: list) -> int:
    """

    :param input_list:
    :return:
    """
    total = 0
    gol = GameOfLife(input_list, crowd=5)
    gol.print_matrix()
    gol.play_game(verbose=False)
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
