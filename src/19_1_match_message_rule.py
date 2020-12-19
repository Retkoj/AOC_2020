import fileinput
import re
from copy import deepcopy
from typing import List


def replace_item_in_list(lst, old, new):
    return [new if val == old else val for val in lst]


def has_integer_values(rule_dict):
    return {key: value for key, value in rule_dict.items()
            if type(value) is list and any([i for i in value if type(i) == int])}


def simplify_str_list(rule_dict, strings_dict):
    # print(strings_dict)
    for key, values in rule_dict.items():
        # if key == 0:
        #     print(values)
        if not strings_dict.get(key, False) and all([True if type(v) == str else False for v in values]):
            strings_dict[key] = f'({"".join(values)})'
            rule_dict[key] = f'({"".join(values)})'
            # rule_dict.pop(key)
        # else:
        #     strings_dict[key] = values
    return strings_dict, rule_dict


def fill_in_rules(rule_dict):
    new_rule_dict = deepcopy(rule_dict)
    new_rule_dict = dict(sorted(new_rule_dict.items(), key=lambda item: item))
    actual_strings = {key: value for key, value in rule_dict.items() if type(value) == str}
    has_integers = True
    while has_integers:
        for rule_nr, actual_s in actual_strings.items():
            new_rule_dict = {key: replace_item_in_list(values, rule_nr, actual_s)
                             if type(values) is list else values
                             for key, values in new_rule_dict.items()
                             }
        actual_strings, new_rule_dict = simplify_str_list(new_rule_dict, actual_strings)
        has_integers = has_integer_values(new_rule_dict)
        print(actual_strings.items())
        # print(new_rule_dict)
        # if has_integers:
        #     actual_strings = {key: value for key, value in new_rule_dict.items() if type(value) == str}
    return actual_strings


def check_rule(rule_zero, messages):
    total = 0
    exact_rule = '^' + rule_zero + '$'
    print(exact_rule)
    for message in messages:
        if re.match(exact_rule, message):
            total += 1
    return total


def process(input_list: List):
    """

    :param input_list:
    :return:
    """
    total = 0
    rule_dict = {}
    index = 0
    line = input_list[index]
    while line:
        line_number = int(line.split(':')[0])
        rule = line.split(':')[1]
        if '"' in rule:
            rule_dict[line_number] = re.findall('"([a-z])"', rule)[0]
        # elif '|' in rule:
        #     rule = rule.replace(' ', '')
        #     or_rule = re.findall('([0-9]+)\|([0-9]+)', rule)[0]
        #     or_rule = [[int(i) for i in list(n)] for n in or_rule]
        #     rule_dict[line_number] = or_rule[0] + ['|'] + or_rule[1]
        else:
            rule_dict[line_number] = [int(i) if i != '|' else i for i in rule.strip().split(' ')]
        index += 1
        line = input_list[index]

    index += 1
    messages = input_list[index:]

    return rule_dict, messages


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    rules, mess = process(lines)
    print(f'Output: {rules}, \n{mess}')
    filled = fill_in_rules(rules)
    print(f'filled: {filled}')
    count_matches = check_rule(filled[0], mess)
    print(f'matched rule zero: {count_matches}')
