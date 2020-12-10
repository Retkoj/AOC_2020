import fileinput


def find_next_jolt(lst):
    """
    Print the product of the 2 numbers whose sum is 2020

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


def process(input_list: list) -> int:
    """

    :param input_list:
    :return:
    """
    total = 0
    return total


if __name__ == '__main__':
    lines = [int(i.strip('\n')) for i in fileinput.input()]
    print(lines[0:10])
    lines.insert(0, 0)
    all, one, three= find_next_jolt(lines)
    print(f'Output: {one * three}')
    print(f'Output: {one} and {three}')
