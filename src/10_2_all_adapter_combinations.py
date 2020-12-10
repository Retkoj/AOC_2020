import fileinput
import re
from functools import reduce
from typing import List

MULITPLICATION = {
    1: 1,
    2: 2,
    3: 4,
    4: 7
}


def differences(lst: List) -> int:
    """
    Challenge: What is the total number of distinct ways you can arrange the adapters to connect the charging outlet
    to your device?

    Calculate the difference between sorted items in lst.
    Find the length of all groups of ones, separated by 3's,
    Reduces and multiplies according to factors in MULIPLICATION dict

    :param lst: List of integers
    :return:
    """
    lines.sort()  # sort list
    diffs = [str(lst[i + 1] - lst[i]) for i in range(0, len(lst) - 1)]  # calculate differences between listitems
    ones = re.findall('(1+)3?', ''.join(diffs))  # Find all (groups of) 1's
    return reduce(lambda a, b: a * b, [MULITPLICATION[len(group)] for group in ones], 1)  # reduce multiply


if __name__ == '__main__':
    lines = [int(i.strip('\n')) for i in fileinput.input()]
    lines.insert(0, 0)
    print(lines)
    total = differences(lines)

    print(f'Output: {total} ')
