from copy import deepcopy
from enum import Enum
from typing import List


class STATE(Enum):
    alive = '#'
    empty = 'L'
    floor = '.'
    not_valid = '-'


class GameOfLife:
    def __init__(self, input_list: List, direct_line_of_sight: bool = False, crowd: int = 4):
        self.original_input = input_list
        self.direct_line_of_sight = direct_line_of_sight
        self.crowd = crowd

        self.matrix = []
        self.new_matrix = []
        self.seat_cells = []

        self.round = 0
        self.current_field = (0, 0)
        self.alive_cells = 0
        self.stabilized = False

        self.length = range(0)
        self.width = range(0)
        self.process_input()

    def process_input(self):
        """Parse string lines to matrix"""
        if self.original_input:
            self.length = range(0, len(self.original_input))
            self.width = range(0, len(self.original_input[0]))

            def get_state(l):
                for i in l:
                    if i == '#':
                        return STATE.alive
                    elif i == 'L':
                        return STATE.empty
                    elif i == '.':
                        return STATE.floor

            self.matrix = [[get_state(item) for item in list(l)] for l in self.original_input]
            self.new_matrix = deepcopy(self.matrix)
            self.get_seat_locations()

    def get_seat_locations(self):
        """all seat locations, active/filled or empty"""
        for x in self.length:
            for y in self.width:
                if self.matrix[x][y] in [STATE.alive, STATE.empty]:
                    self.seat_cells.append((x, y))

    def print_matrix(self):
        for row in self.matrix:
            print([v.value for v in row])

    def reset(self):
        self.process_input()
        self.current_field = (0, 0)
        self.stabilized = False
        self.round = 0
        self.alive_cells = 0

    def get_current_value(self):
        x, y = self.current_field
        return self.matrix[x][y]

    def play_game(self, rounds: int = -1, verbose: bool = False):
        print('playing')
        while (not self.stabilized) and self.round != rounds:
            self.play_round()
            if verbose:
                self.print_matrix()
            if self.stabilized:
                self.count_alive()
                print(f'Stabilized in round{self.round}, Seats occupied: {self.alive_cells}')
            self.round += 1

    def play_round(self):
        print(f'round {self.round}')
        for x, y in self.seat_cells:
            self.current_field = (x, y)
            self.new_matrix[x][y] = self.check_rules()
        if self.new_matrix == self.matrix:
            self.stabilized = True
        self.matrix = deepcopy(self.new_matrix)

    def check_rules(self):
        if self.get_current_value() == STATE.floor:
            return self.get_current_value()
        count_alive = self.check_surrounding_fields()
        if count_alive == 0 and self.get_current_value() == STATE.empty:
            return STATE.alive
        elif count_alive >= self.crowd and self.get_current_value() == STATE.alive:
            return STATE.empty
        else:
            return self.get_current_value()

    def check_surrounding_fields(self):
        if self.direct_line_of_sight:
            indices = self.get_direct_line_of_sight()
            count_alive = sum([1 for x, y in indices if self.matrix[x][y] == STATE.alive])
        else:
            count_alive = self.fields_in_sight()
        return count_alive

    def check_valid(self, x, y):
        if (x, y) != self.current_field and (x, y) in self.seat_cells:
            return True
        return False

    def get_direct_line_of_sight(self):
        """Get the 8 chairs directly connected to current seat"""
        x, y = self.current_field
        indices = []
        for i in [x - 1, x, x + 1]:
            for j in [y - 1, y, y + 1]:
                if self.check_valid(i, j):
                    indices.append((i, j))
        return indices

    def fields_in_sight(self):
        """get all 8 seats in line of sight"""
        x, y = self.current_field
        x_max = max(self.length) + 1
        y_max = max(self.width) + 1

        def quicker_vertical(x_range, y):
            for x in x_range:
                if self.check_valid(x, y):
                    return self.matrix[x][y]
            return STATE.not_valid

        # Vertical line:
        x_lower = quicker_vertical(reversed(range(0, x)), y)
        x_upper = quicker_vertical(range(x + 1, x_max), y)

        def quicker_horizontal(x, y_range):
            for y in y_range:
                if self.check_valid(x, y):
                    return self.matrix[x][y]
            return STATE.not_valid
        # Horizontal line:
        y_lower = quicker_horizontal(x, reversed(range(0, y)))
        y_upper = quicker_horizontal(x, range(y + 1, y_max))

        x_y_indices = [c for c in [x_lower, x_upper, y_lower, y_upper] if c]

        def quicker_diag(x_lst, y_lst):
            x_lst = list(x_lst)
            y_lst = list(y_lst)
            max_index = min(len(x_lst), len(y_lst))
            for i in range(0, max_index):
                x = x_lst[i]
                y = y_lst[i]
                if self.check_valid(x, y):
                    return self.matrix[x][y]
            return STATE.not_valid
        # diagonals:
        diags = [quicker_diag(x_l, y_l) for x_l, y_l in [(reversed(range(0, x)), reversed(range(0, y))),
                                                         (range(x + 1, x_max), reversed(range(0, y))),
                                                         (range(x + 1, x_max), range(y + 1, y_max)),
                                                         (reversed(range(0, x)), range(y + 1, y_max))]]

        return sum([1 for c in x_y_indices + diags if c == STATE.alive])

    def count_alive(self):
        self.alive_cells = sum([sum([1 for seat in row if seat == STATE.alive]) for row in self.matrix])
