import fileinput
import re
from typing import List


def get_most_probable_fields(field_indexes):
    """Assume the input is nice:
    order by length of possible indexes, start with the field that only has 1 index, mark that index as taken
    and eliminate it as the option for other fields
    return a dict with one integer per field"""
    final_indexes = {}
    used_indexes = []
    sorted_by_possibilities = dict(sorted(field_indexes.items(), key=lambda item: len(item[1])))
    for field, indexes in sorted_by_possibilities.items():
        if len(indexes) > 1:
            indexes = [i for i in indexes if i not in used_indexes]
        final_indexes[field] = indexes[0]
        used_indexes.append(indexes[0])
    print(sorted_by_possibilities)
    return final_indexes


def match_fields(rules: dict, your_ticket: List, valid_other_tickets: List):
    """Get the possible fields for an index; i.e. where all tickets' values for that index fit a certain rule
    Can lead to multiple indexes per field"""
    all_tickets = [your_ticket]
    all_tickets.extend(valid_other_tickets)
    fields_indexed = {field: [] for field in rules.keys()}

    for index in range(0, len(your_ticket)):
        values_on_index = [ticket[index] for ticket in all_tickets]
        for field, rule_range in rules.items():
            rule_fits = True
            for value in values_on_index:
                if value not in rule_range:
                    rule_fits = False
            if rule_fits:
                fields_indexed[field].append(index)

    return fields_indexed


def process_not_valid_fields(rules, other_tickets):
    """Remove tickets that have a field that matches none of the rules"""
    valid_other_tickets = []
    invalid_count = 0
    for other_ticket in other_tickets.values():
        valid_values = 0
        for value in other_ticket:
            any_good = False
            for rule_values in rules.values():
                if value in rule_values:
                    any_good = True
            if any_good:
                valid_values += 1
        if valid_values != len(other_ticket):
            invalid_count += 1
        else:
            valid_other_tickets.append(other_ticket)

    return valid_other_tickets, invalid_count


def process(input_list: List):
    """
    Parse input:
    - rules
    - your_ticket
    - other_tickets
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
        rule_tuples_as_int = [tuple(int(i) for i in c) for c in rule_tuples]
        rules[field] = list(range(rule_tuples_as_int[0][0], rule_tuples_as_int[0][1] + 1)) +\
                       list(range(rule_tuples_as_int[1][0], rule_tuples_as_int[1][1] + 1))
        index += 1
        line = input_list[index]

    index += 2  # go to your ticket values
    line = input_list[index]
    your_ticket = [int(val) for val in line.split(',')]

    for i, ticket in enumerate(input_list[index + 3:]):
        other_tickets[i] = [int(val) for val in ticket.split(',')]

    return rules, your_ticket, other_tickets


def get_output(field_indexes, yt):
    """apply indexes to your_ticket"""
    product = 1
    for field, index in field_indexes.items():
        if field.startswith('departure'):
            product *= yt[index]
    return product


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    # print(lines[0:50])
    r, yt, ot = process(lines)
    valid_others, inv_count = process_not_valid_fields(r, ot)
    print(f'{len(valid_others)} valid and {inv_count} invalid other tickets')
    field_indexes = match_fields(r, yt, valid_others)
    print(f'indexes: {field_indexes}')
    final_field_indexes = get_most_probable_fields(field_indexes)
    print(f'final indexes: {final_field_indexes}')
    output = get_output(final_field_indexes, yt)
    print(f'Output: {output}')
    sorted_final = dict(sorted(final_field_indexes.items(), key=lambda item: item[1]))
    for key, index in sorted_final.items():
        print(f'{key}: {index} - {yt[index]}')
