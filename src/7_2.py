import fileinput
import re
from typing import List


def get_outer_bags(bag_requirements: dict, target_bag: str) -> List:
    return [color for color, sub_bags in bag_requirements.items() if sub_bags.get(target_bag, False)]


def get_inner_bags(bag_requirements: dict, target_bag: str, factor: int = 1):
    """

    :param bag_requirements:
    :param target_bag:
    :param factor:
    :return:
    """
    inner_bags = bag_requirements[target_bag]
    factored_inner_bags = {key: int(value) * factor for key, value in inner_bags.items()}
    count = sum([int(n) for color, n in factored_inner_bags.items()])
    return factored_inner_bags, count


def loop_exhaustive_inner(bag_requirements: dict, target_bag: str) -> int:
    """
    Find all direct inner bags for the target bag (shiny_gold in case of day 7_2)
    Multiply the numbers by the parents number and sum all inner bags together.
    Then treat all found inner bags as target bags themselves and repeat process
    Script stops if none of the inner bags have any inner bags themselves.

    :param bag_requirements:
    :param target_bag:
    :return:
    """
    current_dict, total_count = get_inner_bags(bag_requirements, target_bag)
    not_exhausted = True
    while not_exhausted:
        tmp_dict = {}
        for bag, factor in current_dict.items():
            l, tmp_count = get_inner_bags(bag_requirements, bag, int(factor))
            # Take into account that a inner bag can be a inner bag to multiple outer bags
            # Sum the individual factored inner bag counts when updating the total dictionary
            tmp_dict = {key: int(tmp_dict.get(key, 0)) + int(l.get(key, 0))
                        for key in list(l.keys()) + list(tmp_dict.keys())}
            total_count += tmp_count
        current_dict = tmp_dict
        if len(current_dict.keys()) == 0:
            not_exhausted = False
    return total_count


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
            if bag and bag.strip(' ') != "no other bags":
                bag = bag.lower()
                parsed_bag = re.findall('([0-9]+) ([a-z]+ [a-z]+) ([a-z]+)', bag)
                if parsed_bag:
                    parsed_bag = parsed_bag[0]
                    n_bags = parsed_bag[0]
                    bag_color = parsed_bag[1].replace(' ', '_')
                    bag_requirements[outer_bag][bag_color] = n_bags
    return bag_requirements


if __name__ == '__main__':
    lines = [i.strip('\n').rstrip('.') for i in fileinput.input()]
    output = process(lines)
    inner_bags_count = loop_exhaustive_inner(output, "shiny_gold")
    print(f'count: {inner_bags_count}')
