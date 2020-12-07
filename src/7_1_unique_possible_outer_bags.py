import fileinput
import re
from typing import List


def get_outer_bags(bag_requirements: dict, current_inner_bag: str) -> List:
    """
    Get outer bags that can contain the current inner bag
    :param bag_requirements: Dict of bag requirements
    :param current_inner_bag: String with current inner bag's color
    :return: List of outer bags that can contain current_target_bag
    """
    return [color for color, sub_bags in bag_requirements.items() if sub_bags.get(current_inner_bag, False)]


def loop_exhaustive_outer(bag_requirements: dict, target_bag: str) -> List:
    """
    Goal of the challenge: How many outer bags could contain the target bag (shiny_gold in case of day 7_1)?

    Current function finds all direct outer bags for the target bag
    Then treat all found outer bags as target bags themselves and list their respective outer bags.
    Script stops if none of the outer bags have any outer bags themselves.

    :param bag_requirements: Dict of bag requirements
    :param target_bag: String with the color of the inner bag in questions (shiny_gold in case of day 7_1)
    :return: List of all found outer bags (may contain duplicates)
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
    Put all bag requirements in a dictionary where the key is the outer bag's color and the value is a dictionary
    containing the inner bags' colors as keys and the requirement amount of the inner bag as value.

    e.g.:
    'dotted blue bags contain 5 wavy green bags, 3 pale beige bags'

    is parsed to:

    'dotted_blue': {
        'wavy_green': '5',
        'pale_beige': '3'
    }

    :param input_list: list of bag requirements as strings
    :return: Dictionary of requirements
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
    requirements = process(lines)
    outer_bags_all = loop_exhaustive_outer(requirements, "shiny_gold")
    print(f'All possible outer bags for shiny gold: {outer_bags_all}\n'
          f'All unique outer bags: {set(outer_bags_all)}\n'
          f'Count of unique outer bags for shiny gold: {len(set(outer_bags_all))}')
