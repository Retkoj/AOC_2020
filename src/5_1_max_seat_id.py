import fileinput
from math import floor, ceil


def process(lst):
    """
    See cleaner implementation in 5_2[..].py
    :param lst:
    :return:
    """
    seat_dict = {}
    max_ID = 0
    for seat in lst:
        min_bound = 0
        max_bound = 127
        row_no = 0
        s_min = 0
        s_max = 7
        seat_no = 0
        for i, letter in enumerate(seat):
            print(seat)
            if i < 7:
                if letter == 'F':  # lower
                    max_bound = floor((max_bound + min_bound) / 2)
                if letter == 'B':  # upper
                    min_bound = ceil((max_bound + min_bound) / 2)
                if i == 6:
                    row_no = max_bound if letter == 'F' else min_bound
            else:
                if letter == 'L':
                    s_max = floor((s_max + s_min) / 2)
                if letter == 'R':  # upper
                    s_min = ceil((s_max + s_min) / 2)
                if i == 9:
                    seat_no = s_max if letter == 'R' else s_min
                    id = (row_no * 8) + seat_no
                    max_ID = id if id >= max_ID else max_ID
        seat_dict[seat] = {
            'row_no': row_no,
            'seat_no': seat_no,
            'seat_ID': (row_no * 8) + seat_no
        }
    print(f'max id {max_ID}')
    return seat_dict


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    seat_dict = process(lines)
    print(seat_dict)
    print(max([value['seat_ID'] for key, value in seat_dict.items()]))


