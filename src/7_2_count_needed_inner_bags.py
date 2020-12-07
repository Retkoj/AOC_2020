import fileinput
import re
from datetime import datetime
from typing import List


def get_outer_bags(bag_requirements: dict, current_inner_bag: str) -> List:
    """
    Get outer bags that can contain the current inner bag
    :param bag_requirements: Dict of bag requirements
    :param current_inner_bag: String with current inner bag's color
    :return: List of outer bags that can contain current_target_bag
    """
    return [color for color, sub_bags in bag_requirements.items() if sub_bags.get(current_inner_bag, False)]


def get_inner_bags(bag_requirements: dict, current_outer_bag: str, factor: int = 1):
    """
    :param bag_requirements: bag_requirements: Dict of bag requirements
    :param current_outer_bag: String with current outer bag's color
    :param factor: How many of current outer bags are needed
    :return:
    """
    inner_bags = bag_requirements[current_outer_bag]
    factored_inner_bags = {key: int(value) * factor for key, value in inner_bags.items()}
    count = sum([int(n) for color, n in factored_inner_bags.items()])
    return factored_inner_bags, count


def loop_exhaustive_inner(bag_requirements: dict, target_bag: str) -> int:
    """
    Challenge: How many inner bags do you have to buy for your target bag (shiny_gold)?

    Find all direct inner bags for the target bag (shiny_gold in case of day 7_2)
    Multiply the numbers by the parents number and sum all inner bags together.
    Then treat all found inner bags as target bags themselves and repeat process
    Script stops if none of the inner bags have any inner bags themselves.

    e.g.:
    shiny gold bags contain 2 dark red bags.
    dark red bags contain 2 dark orange bags.
    dark orange bags contain 2 dark yellow bags.

    gives: 2 red + (2 red * 2) orange + (2 red * 2 orange * 2) yellow = 14 inner bags for 1 shiny gold bag

    :param bag_requirements:
    :param target_bag:
    :return:
    """
    current_dict, total_count = get_inner_bags(bag_requirements, target_bag)
    not_exhausted = True
    while not_exhausted:
        tmp_dict = {}
        for bag, factor in current_dict.items():
            d, tmp_count = get_inner_bags(bag_requirements, bag, int(factor))
            # Take into account that a inner bag can be a inner bag to multiple outer bags
            # Sum the individual factored inner bag counts when updating the total dictionary
            tmp_dict = {key: int(tmp_dict.get(key, 0)) + int(d.get(key, 0))
                        for key in list(d.keys()) + list(tmp_dict.keys())}
            total_count += tmp_count
        current_dict = tmp_dict
        if len(current_dict.keys()) == 0:
            not_exhausted = False
    return total_count


def process(input_list: list) -> dict:
    """
    Put all bag requirements in a dictionary where the key is the outer bag's color and the value is a dictionary
    containing the inner bags' colors as keys and the requirement amount of the inner bag as value.

    e.g.:
    'dotted blue bags contain 5 wavy green bags, 3 pale beige bags'

    is parsed to:

    'dotted_blue': {
        'wavy_green': 5,
        'pale_beige': 3
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
                parsed_bag = re.findall('([0-9]+) ([a-z]+ [a-z]+) ([a-z]+)', bag.lower())
                if parsed_bag:
                    n_bags = parsed_bag[0][0]
                    bag_color = parsed_bag[0][1].replace(' ', '_')
                    bag_requirements[outer_bag][bag_color] = int(n_bags)
    return bag_requirements


if __name__ == '__main__':
    lines = [i.strip('\n').rstrip('.') for i in fileinput.input()]
    requirements = process(lines)
    inner_bags_count = loop_exhaustive_inner(requirements, "shiny_gold")
    print(f'Number of inner bags needed: {inner_bags_count}')
