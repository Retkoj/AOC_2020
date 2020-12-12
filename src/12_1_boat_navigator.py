import fileinput

import re
from typing import List

from BoatNavigatorWaypoint import Direction


class BoatNavigator:
    def __init__(self, input_instruction: List):
        self.original_instructions = input_instruction

        self.base_direction = Direction.EAST
        self.current_direction = Direction.EAST
        self.current_number = 0

        self.location = {
            Direction.NORTH: 0,
            Direction.SOUTH: 0,
            Direction.EAST: 0,
            Direction.WEST: 0
        }
        self.opposites = {
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
        }
        self.execute = {
            Direction.NORTH: self.move_NSWE,
            Direction.SOUTH: self.move_NSWE,
            Direction.EAST: self.move_NSWE,
            Direction.WEST: self.move_NSWE,
            Direction.RIGHT: self.move_LR,
            Direction.LEFT: self.move_LR,
            Direction.FORWARD: self.move_forward
        }

    def parse_instruction(self, instruction):
        """e.g. 'R4 -> Direction.RIGHT 4"""
        parsed = re.match('([A-Z]{1})([0-9]+)', instruction)
        command, number = parsed.groups()
        self.current_direction = Direction(command)
        self.current_number = int(number)

    def move(self):
        for instruction in self.original_instructions:
            self.parse_instruction(instruction)
            self.execute[self.current_direction]()
        print(self.location)

    def move_NSWE(self):
        self.location[self.current_direction] += self.current_number
        self.location[self.opposites[self.current_direction]] -= self.current_number

    def move_LR(self):
        turns = int(self.current_number / 90)
        directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        if self.current_direction == Direction.LEFT:
            directions = list(reversed(directions))
        i = directions.index(self.base_direction)
        reorder = directions[i:] + directions[0:i]
        self.base_direction = reorder[turns]

    def move_forward(self):
        self.location[self.base_direction] += self.current_number
        self.location[self.opposites[self.base_direction]] -= self.current_number


def process(input_list: list) -> int:
    """

    :param input_list:
    :return:
    """
    total = 0
    bn = BoatNavigator(input_list)
    bn.move()
    total = sum([val for val in bn.location.values() if val > 0])
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
