import fileinput


def get_seat(lst):
    lst.sort()
    diffs = []
    for i in range(0, len(lst) - 1):
        diffs.insert(i, lst[i + 1] - lst[i])
        if lst[i + 1] - lst[i] == 2:
            print(f'index {i}, {lst[i:i+2]}')


def binary_implementation(lst):
    """
    Converts the seatdescription to the binary description and then to decimal. Finally the seat ID is calculated
    by the formula `(row number * 8) + seat number`

    Example:
    Seat on ticket: 'BFBFFBBLLR'
    Row number: '1010011' -> 83
    Seat number: '001' - > 1
    Seat ID: (83 * 8) + 1 = 665

    :param lst: List of seat numbers as listed on the tickets
    :return: Dict with row number, seat number, seat ID per ticket
    """
    seat_dict = {}
    for ticket in lst:
        row_no = int(ticket[0:7].replace('F', '0').replace('B', '1'), 2)
        seat_no = int(ticket[7:10].replace('L', '0').replace('R', '1'), 2)
        seat_dict[ticket] = {
            'row_no': row_no,
            'seat_no': seat_no,
            'seat_ID': (row_no * 8) + seat_no
        }
    return seat_dict


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]

    seats = binary_implementation(lines)
    print('Maximum seat ID in list: {}'.format(max([value['seat_ID'] for key, value in seats.items()])))
    get_seat([value['seat_ID'] for key, value in seats.items()])


