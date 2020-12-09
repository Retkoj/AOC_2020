import fileinput


def find_sum(lst, output_num):
    """
    Print the product of the 2 numbers whose sum is 2020

    :param lst: list of integers
    """
    for i, current_number in enumerate(lst):
        for j, other_number in enumerate(lst):
            if j != i and (current_number + other_number == output_num):
                return True
    return False


def process(input_list: list) -> int:
    """

    :param input_list:
    :return:
    """
    total = 0
    preamble_length = 25
    preamble = input_list[:25]
    for i in range(25, len(input_list)):
        if not find_sum(preamble, input_list[i]):
            return input_list[i]
        preamble.pop(0)
        preamble.append(input_list[i])
    return total


if __name__ == '__main__':
    lines = [int(i.strip('\n')) for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
