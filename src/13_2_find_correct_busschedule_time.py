import fileinput
from functools import reduce


def find_time(dct, time=0, increment=1):
    """
    Return the time at which all buses in the dictionary fit their relative departure time.

    :param dct: busschedule dictionary
    :param time: time to start looping at
    :param increment: value with which to increment time between loops
    :return: time that fits the requirements for all buses
    """
    found_t = False
    while not found_t:
        all_good = True
        for i, bus in dct.items():
            if not ((time + i) % bus == 0):
                all_good = False
        if all_good:
            found_t = True
        else:
            time += increment
    return time


def find_busschedule_iteratively(dct):
    """
    Challenge: What is the earliest timestamp such that all of the listed bus IDs depart at offsets matching their
    positions in the list?

    Goes through the list of buses in slices, determining the correct departure time iteratively using find_time()
    e.g.:
    { 17: 0, 13: 2, 19: 3}
    would be processed in the slices:
    { 17: 0, 13: 2}
    and
    { 17: 0, 13: 2, 19: 3}

    and fed to the find_time function with
    - the starttime: 0 or derived from a previous run, in this case the first run returns 102
    - the value with which to increment the time; this is the first busnumber for the first run (17) and
      221 (17 * 13) for the next. If there were more numbers in the dictionary, the next would be 4199 (17 * 13 * 19)

    :param dct: busschedule as dictionary
    :return: correct starttime for the busschedule to be true
    """
    buses = list(dct.keys())
    increments = buses[0]
    time = 0
    for i in range(2, len(buses) + 1):
        tmp_lst = buses[0:i]
        tmp_dict = {i: bus for bus, i in dct.items() if bus in tmp_lst}
        time = find_time(tmp_dict, time, increments)
        increments = reduce(lambda a, b: a * b, tmp_lst, 1)

    return time


def process(input_list: list) -> dict:
    """
    return the list of buses in the form:
    { busnumber: relative_departure_time}
    where busnumber signifies time between runs
    e.g.
    { 17: 0, 13: 2, 19: 3}
    :param input_list: List with two entries of which the second is the relative busschedule
    :return: dictionary
    """
    bus_dict = {int(bus): i for i, bus in enumerate(input_list[1].split(',')) if bus != 'x'}

    return bus_dict


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    buses_dict = process(lines)
    correct_time = find_busschedule_iteratively(buses_dict)
    print(f'Output: {correct_time}')
