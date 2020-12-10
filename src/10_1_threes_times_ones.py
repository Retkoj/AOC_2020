import fileinput
from typing import List


def quick_and_dirty(lst):
    """
    Challenge: If you use every adapter in your bag at once, what is the distribution of joltage differences between
    the charging outlet, the adapters, and your device?
    Return n1 * n3 jolts.

    Current function counts all instances of 1 diffs and 3 diffs, given the lowest jumps

    :param lst: list of integers
    """
    all_numbers = []
    counts_one = 0
    counts_three = 1
    lst.sort()
    for i, current_number in enumerate(lst):
        possibles = []
        for j, other_number in enumerate(lst):
            if j != i and (other_number - current_number in list(range(1, 4))):
                possibles.append(other_number)
        if possibles:
            lowest = min(possibles)
            all_numbers.append(lowest)
            if lowest - current_number == 1:
                counts_one += 1
            elif lowest - current_number == 3:
                counts_three += 1
    return all_numbers, counts_one, counts_three


def quicker(lst: List) -> (int, int):
    """
    Challenge: If you use every adapter in your bag at once, what is the distribution of joltage differences between
    the charging outlet, the adapters, and your device?
    Return n1 * n3 jolts.

    Current function calculates the difference between sorted items in lst and count number of ones and threes

    :param lst: List of integers
    :return:
    """
    lines.sort()  # sort list
    diffs = [lst[i + 1] - lst[i] for i in range(0, len(lst) - 1)]  # diff between item and the next item
    ones = len([o for o in diffs if o == 1])  # count ones
    threes = len([t for t in diffs if t == 3])  # count threes
    return ones, threes


if __name__ == '__main__':
    lines = [int(i.strip('\n')) for i in fileinput.input()]
    print(lines[0:10])
    lines.insert(0, 0)
    # all, one, three= find_next_jolt(lines)
    one, three = quicker(lines)
    print(f'Output: {one * three}')
    print(f'Output: {one} and {three}')
