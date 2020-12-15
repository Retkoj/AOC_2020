import fileinput
from typing import List


def process(input_list: List) -> int:
    """
    In this game, the players take turns saying numbers. They begin by taking turns reading from a list of starting
    numbers (your puzzle input). Then, each turn consists of considering the most recently spoken number:

    - If that was the first time the number has been spoken, the current player says 0.
    - Otherwise, the number had been spoken before; the current player announces how many turns apart the number is
    from when it was previously spoken.

    e.g. input: [0, 3, 6]
    Gives the first 10 rounds:
    0 3 6 0 3 3 1 0 4 0

    Challenge: Find the 2020th number
    :param input_list:
    :return:
    """
    last_index_dict = {int(value): int(index) + 1 for index, value in enumerate(input_list)}
    prev_num = input_list[-1]
    for i in range(len(input_list), 2020):
        if i == last_index_dict[prev_num]:
            prev_num = 0
        else:
            new_num = i - last_index_dict[prev_num]
            last_index_dict[prev_num] = i
            prev_num = new_num
            if not last_index_dict.get(new_num, False):
                last_index_dict[new_num] = i + 1
    return prev_num


if __name__ == '__main__':
    lines = [int(n) for n in [i.strip('\n') for i in fileinput.input()][0].split(',')]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
