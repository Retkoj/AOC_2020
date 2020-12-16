import fileinput
import re
from typing import List


def process_not_valid_fields(rules, other_tickets):
    invalid_sum = 0

    all_values = [value for sublist in other_tickets.values() for value in sublist]
    for other_ticket in other_tickets.values():
        for value in other_ticket:
            any_good = False
            for rule in rules.values():
                if any([True if value in range(rule_range[0], rule_range[1] + 1) else False for rule_range in rule]):
                    any_good = True
            if not any_good:
                invalid_sum += value
    return invalid_sum


def process(input_list: List):
    """

    :param input_list:
    :return:
    """
    rules = {}
    other_tickets = {}
    index = 0
    line = input_list[index]
    while line:  # loops til classes are finished by empty line
        field, values = line.split(':')
        rule_tuples = re.findall('([0-9]+)-([0-9]+)', values)
        rules[field] = [tuple(int(i) for i in c) for c in rule_tuples]
        index += 1
        line = input_list[index]

    index += 2  # go to your ticket values
    line = input_list[index]
    your_ticket = [int(val) for val in line.split(',')]

    for i, ticket in enumerate(input_list[index + 3:]):
        other_tickets[i] = [int(val) for val in ticket.split(',')]

    return rules, your_ticket, other_tickets


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:50])
    r, yt, ot = process(lines)
    print(r)
    print(yt)
    print(ot)
    output = process_not_valid_fields(r, ot)
    print(f'Output: {output}')
