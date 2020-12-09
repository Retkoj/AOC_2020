import fileinput
from typing import List


def find_sum(input_list: List, output_num: int) -> bool:
    """
    Returns True if the sum of the 2 separate numbers in the list equals output_num

    e.g.:
    input_list = [3, 6, 9, 1, 4]
    output_num = 4
    True -> 3 + 1 = 4
    output_num = 2
    False -> no numbers sum to 2

    :param input_list: list of integers
    :param output_num: number to check the sum against
    """
    for i, current_number in enumerate(input_list):
        for j, other_number in enumerate(input_list):
            if j != i and (current_number + other_number == output_num):
                return True
    return False


def step_wise_sum(input_list: List, output_num: int) -> List:
    """
    Calculate the accumulative sum of different continuous slices of the lst.
    Returns the slice that sums up to output_num

    e.g.
    input_list = [1, 5, 2, 9, 44, 53]
    output_num = 55
    returns: [2, 9, 44]
    output_num = 3
    returns: [] (no continuous slice sums to 3)

    :param input_list: list of integers
    :param output_num: integer of sum to be found
    :return: Slice of input_list that sums to output_num
    """
    for i, num in enumerate(input_list):
        slice_sum = num
        for j in range(i + 1, len(input_list) - 1):
            slice_sum += input_list[j]
            if slice_sum == output_num:
                return input_list[i: j + 1]
    return []


def process(input_list: list, preamble_length: int = 25) -> List:
    """
    - Find the 2 numbers in the preamble range of the list that sum up to the next number in the list
    - if none are found then run through the list to find a continuous slice that adds up to the number
      - Slice is returned if applicable

    :param input_list: List of integers
    :param preamble_length: Length of list to use in validating next number
    :return: List of integers
    """
    preamble = input_list[:preamble_length]
    for i in range(preamble_length, len(input_list)):
        if not find_sum(preamble, input_list[i]):
            return step_wise_sum(input_list, input_list[i])
        preamble.pop(0)
        preamble.append(input_list[i])
    return []


if __name__ == '__main__':
    lines = [int(i.strip('\n')) for i in fileinput.input()]
    print(lines[0:20])
    l = process(lines)
    print(f'Sum of lowest and highest: {min(l) + max(l)}')
    print(f'lowest: {min(l)} and highest:  {max(l)}')
