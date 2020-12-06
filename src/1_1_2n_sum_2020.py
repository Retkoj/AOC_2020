import fileinput


def sum_and_product(lst):
    """
    Print the product of the 2 numbers whose sum is 2020

    :param lst: list of integers
    """
    for i, current_number in enumerate(lst):
        for j, other_number in enumerate(lst):
            if j != i and (current_number + other_number == 2020):
                print(f'{i}: {current_number} + {j}: {other_number} = {current_number + other_number}\n'
                      f'{current_number} * {other_number} = {current_number * other_number}')


if __name__ == '__main__':
    lines = [int(i.strip('\n')) for i in fileinput.input()]
    sum_and_product(lines)
