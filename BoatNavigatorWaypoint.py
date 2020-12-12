import re
from enum import Enum
from typing import List


class Direction(Enum):
    EAST = 'E'
    WEST = 'W'
    NORTH = 'N'
    SOUTH = 'S'
    RIGHT = 'R'
    LEFT = 'L'
    FORWARD = 'F'


class BoatNavigatorWaypoint:
    def __init__(self, input_instruction: List):
        self.move_instructions = input_instruction

        self.current_direction = Direction.EAST
        self.current_number = 0

        self.waypoint = {
            Direction.NORTH: 1,
            Direction.SOUTH: -1,
            Direction.EAST: 10,
            Direction.WEST: -10
        }
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

    def sail_away(self):
        """Loop through and parse the instructions and adjust location and waypoint along the way"""
        for instruction in self.move_instructions:
            self.parse_instruction(instruction)
            self.execute[self.current_direction]()

    def move_NSWE(self):
        """Update the waypoint of the current direction with +current number.
        The opposite direction is update with -current number
        e.g. 'N1' on waypoint:
        {
            Direction.NORTH: 1,
            Direction.SOUTH: -1,
            ...
        }
        Becomes:
        {
            Direction.NORTH: 2,
            Direction.SOUTH: -2,
            ...
        }
        """
        self.waypoint[self.current_direction] += self.current_number
        self.waypoint[self.opposites[self.current_direction]] -= self.current_number

    def move_LR(self):
        """Turns the waypoint left (counterclockwise) or right (clockwise)
        Assumed turn is a multiple of 90 and less than 360
        e.g. 'L1' on:
         {
            Direction.NORTH: 1,
            Direction.EAST: 10,
            Direction.SOUTH: -1,
            Direction.WEST: -10
         }
         Becomes:
         {
            Direction.NORTH: 10,
            Direction.EAST: -1,
            Direction.SOUTH: -10
            Direction.WEST: 1,
         }
        """
        turns = int(self.current_number / 90)
        directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        if self.current_direction == Direction.LEFT:
            directions = list(reversed(directions))  # Make directions list counterclockwise
        tmp_waypoint = {}
        for current_wp_direction, current_wp_value in self.waypoint.items():
            i = directions.index(current_wp_direction)
            current_wp_first = directions[i:] + directions[0:i]
            tmp_waypoint[current_wp_first[turns]] = current_wp_value
        self.waypoint = tmp_waypoint

    def move_forward(self):
        """Move forward by multiplying the waypoint and adding it to the current location.
        Only looks at positive points in the waypoint, zo avoid zeroing out the move"""
        num = self.current_number
        added_movement = {key: (val * num) for key, val in self.waypoint.items() if val > 0}
        for key, val in added_movement.items():
            self.location[key] += val
            self.location[self.opposites[key]] -= val
