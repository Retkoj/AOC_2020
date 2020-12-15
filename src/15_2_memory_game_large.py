import fileinput
from datetime import datetime
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

    Challenge: Find the 30000000th number

    :param input_list:
    :return:
    """
    start_time = datetime.now()
    last_index_dict = {int(value): int(index) + 1 for index, value in enumerate(input_list)}
    prev_num = input_list[-1]  # Start with the last input number
    i = len(input_list)  # Start at the index after the input numbers
    while i < 30000000:
        new_num = i - last_index_dict[prev_num]
        last_index_dict[prev_num] = i
        while not last_index_dict.get(new_num, False):  # loop for case: 0 is not in the input list
            i += 1  # move to the next index
            last_index_dict[new_num] = i  # the next index is the first index of new_num
            new_num = 0  # first index means the next value is 0
        prev_num = new_num  # Continue normal loop
        i += 1
    end_time = datetime.now()
    print(f'run time: {end_time - start_time}')
    return prev_num


if __name__ == '__main__':
    lines = [int(n) for n in [i.strip('\n') for i in fileinput.input()][0].split(',')]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
