import fileinput
import re
from typing import List


def get_outer_bags(bag_requirements: dict, target_bag: str) -> List:
    return [color for color, sub_bags in bag_requirements.items() if sub_bags.get(target_bag, False)]


def loop_exhaustive_outer(bag_requirements: dict, target_bag: str) -> List:
    """
    Find all direct outer bags for the target bag (shiny_gold in case of day 7_1)
    Then treat all found outer bags as target bags themselves.
    Script stops if none of the outer bags have any outer bags themselves.

    :param bag_requirements:
    :param target_bag:
    :return:
    """
    final_list = []
    not_exhausted = True
    current_list = get_outer_bags(bag_requirements, target_bag)
    while not_exhausted:
        final_list += current_list
        tmp_list = []
        for bag in current_list:
            tmp_list += get_outer_bags(bag_requirements, bag)
        current_list = tmp_list
        if len(current_list) == 0:
            not_exhausted = False
    return final_list


def process(input_list: list) -> dict:
    """
    Put all bag requirements in a dictionary

    e.g.:
    'dotted blue bags contain 5 wavy green bags, 3 pale beige bags'
    if parsed to:
    'dotted_blue': {
        'wavy_green': '5',
        'pale_beige': '3'
    }

    :param input_list: list of bag requirements
    :return:
    """
    bag_requirements = {}
    for bag_requirement in input_list:
        outer_bag = bag_requirement.split(' bags ')[0].replace(' ', '_').lower()
        bag_requirements[outer_bag] = {}

        sub_bags = bag_requirement.split(' contain ')[1].split(', ')
        for bag in sub_bags:
            print(bag)
            if bag and bag.strip(' ') != "no other bags":
                bag = bag.lower()
                parsed_bag = re.findall('([0-9]+) ([a-z]+ [a-z]+) ([a-z]+)', bag)
                print(parsed_bag)
                if parsed_bag:
                    parsed_bag = parsed_bag[0]
                    n_bags = parsed_bag[0]
                    bag_color = parsed_bag[1].replace(' ', '_')
                    print(f'color: {bag_color}, number: {n_bags}')
                    bag_requirements[outer_bag][bag_color] = n_bags
            else:
                print('not parsed')
    return bag_requirements


if __name__ == '__main__':
    lines = [i.strip('\n').rstrip('.') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
    outer_bags_all = loop_exhaustive_outer(output, "shiny_gold")
    print(f'all outers {outer_bags_all}\n'
          f'set: {set(outer_bags_all)}\n'
          f'count: {len(set(outer_bags_all))}')
