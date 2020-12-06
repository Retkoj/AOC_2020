import fileinput


def sum_and_product(lst):
    """
    Print the product of the 3 numbers whose sum is 2020

    :param lst: list of integers
    """
    for i, first_number in enumerate(lst):
        for j, second_number in enumerate(lst):
            for k, third_number in enumerate(lst):
                if len({i, j, k}) == len((i, j, k)) and (first_number + second_number + third_number == 2020):
                    print(f'{i}: {first_number} + {j}: {third_number} + {k}: {third_number} = '
                          f'{first_number + second_number + third_number}\n'
                          f'{first_number} * {second_number}  * {third_number} ='
                          f'{first_number * second_number * third_number}')


if __name__ == '__main__':
    lines = [int(i.strip('\n')) for i in fileinput.input()]
    sum_and_product(lines)
