import fileinput

from BoatNavigatorWaypoint import BoatNavigatorWaypoint


def process(input_list: list) -> int:
    """

    :param input_list:
    :return:
    """
    bn = BoatNavigatorWaypoint(input_list)
    bn.sail_away()
    print(bn.location)
    total = sum([val for val in bn.location.values() if val > 0])
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
