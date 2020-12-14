import fileinput


def find_bus(lst, goal):
    """
    Which bus is the first bus to arrive when you get to the ferry terminal?
    busnumber signifies time between runs

    :param lst: list of buses
    :param goal: time you're arriving
    :return: time to wait, busnumber to wait for
    """
    quickest = goal
    best_bus = 0
    for bus in lst:
        diff = bus - (goal % bus) if (goal % bus) > 0 else 0
        print(f'{bus} {diff}')
        if diff < quickest:
            best_bus = bus
            quickest = diff
    return quickest, best_bus


def process(input_list: list):
    """

    :param input_list:
    :return:
    """
    total = 0
    goal = int(input_list[0])
    bus_list = [int(bus) for bus in input_list[1].split(',') if bus != 'x']

    return bus_list, goal


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    buses, goal = process(lines)
    output, bbus = find_bus(buses, goal)
    print(f'Output: {output} * bus {bbus} = {8*821}')
