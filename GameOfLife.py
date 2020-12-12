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
        self.cached_line_of_sight = {}

        self.round = 0
        self.current_field = (0, 0)
        self.alive_cells = 0
        self.stabilized = False

        self.length_max = 0
        self.length_range = range(0)
        self.width_max = 0
        self.width_range = range(0)
        self.process_input()

    def process_input(self):
        """Parse string lines to matrix"""
        if self.original_input:
            self.length_max = len(self.original_input)
            self.length_range = range(0, self.length_max)
            self.width_max = len(self.original_input[0])
            self.width_range = range(0, self.width_max)

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
        for x in self.length_range:
            for y in self.width_range:
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
        """Get the state of the current seat"""
        x, y = self.current_field
        return self.matrix[x][y]

    def play_game(self, rounds: int = -1, verbose: bool = False):
        print('Commence operation \'stoelendans\'')
        while (not self.stabilized) and self.round != rounds:
            self.play_round()
            if verbose:
                self.print_matrix()
            if self.stabilized:
                self.count_alive()
                print(f'Stabilized in round{self.round}, Seats occupied: {self.alive_cells}')
            self.round += 1

    def play_round(self):
        """Loop through all seats in the matrix and update state in new_matrix.
        if the new_matrix is the same as matrix, the stabilized becomes True
        else, set matrix to new_matrix"""
        print(f'round {self.round}')
        for x, y in self.seat_cells:
            self.current_field = (x, y)
            self.new_matrix[x][y] = self.process_current_seat()
        if self.new_matrix == self.matrix:
            self.stabilized = True
        self.matrix = deepcopy(self.new_matrix)

    def process_current_seat(self):
        """Get the count of alive (filled) seats from LoS,
        check and return new seat state"""
        if self.get_current_value() == STATE.floor:  # Since we're only looping through seat cells, this is redundant
            return self.get_current_value()
        count_alive = self.check_surrounding_fields()
        return self.check_rules(count_alive)

    def check_rules(self, count_alive: int):
        """
        - If a seat is empty and all seats in LoS are empty, seat gets filled
        - If seat is filled, and `self.crowd` or more seats are filled, seat becomes empty
        - Otherwise; seat stays the same state
        :return: state
        """
        if count_alive == 0 and self.get_current_value() == STATE.empty:
            return STATE.alive
        elif count_alive >= self.crowd and self.get_current_value() == STATE.alive:
            return STATE.empty
        else:
            return self.get_current_value()

    def check_surrounding_fields(self):
        """Get the coordinates of the chairs in the (direct) Line of Sight (LoS).
        Saves the coordinates in LoS per seat for the next run.
        :return: Count of seats with state.ALIVE for current seat
        """
        if self.cached_line_of_sight.get(self.current_field, None) is None:
            if self.direct_line_of_sight:
                self.cached_line_of_sight[self.current_field] = self.get_direct_line_of_sight()
            else:
                self.cached_line_of_sight[self.current_field] = self.fields_in_sight()
        indices = self.cached_line_of_sight[self.current_field]
        count_alive = sum([1 for x, y in indices if self.matrix[x][y] == STATE.alive])
        return count_alive

    def check_valid_LOS_coordinate(self, x, y):
        """A valid Line of Sight coordinate is a seat (state.ALIVE or state.EMPTY) and is not the current seat"""
        if (x, y) != self.current_field and (x, y) in self.seat_cells:
            return True
        return False

    def get_direct_line_of_sight(self):
        """Get the 8 chairs directly connected to current seat"""
        x, y = self.current_field
        indices = []
        for i in [x - 1, x, x + 1]:
            for j in [y - 1, y, y + 1]:
                if self.check_valid_LOS_coordinate(i, j):
                    indices.append((i, j))
        return indices

    def fields_in_sight(self):
        """get all 8 seats in line of sight, if any"""
        indices = self.horizontal_fields_in_sigth()
        indices += self.vertical_fields_in_sight()
        indices += self.diagonal_fields_in_sight()
        return indices

    def vertical_fields_in_sight(self):
        """Gets the coordinates of any seats in the vertical line of sight"""
        current_x, current_y = self.current_field

        def get_valid_vertical_coords(x_range) -> tuple or None:
            """Returns the first valid coordinate it comes across"""
            for tmp_x in x_range:
                if self.check_valid_LOS_coordinate(tmp_x, current_y):
                    return (tmp_x, current_y)
            return None

        # Vertical line:
        x_lower = get_valid_vertical_coords(reversed(range(0, current_x)))
        x_upper = get_valid_vertical_coords(range(current_x + 1, self.length_max))
        return [coords for coords in [x_lower, x_upper] if coords is not None]  # None = no seats in that line of sight

    def horizontal_fields_in_sigth(self):
        """Gets the coordinates of any seats in the horizontal line of sight"""
        current_x, current_y = self.current_field

        def get_valid_horizontal_coords(y_range) -> tuple or None:
            """Returns the first valid coordinate it comes across"""
            for tmp_y in y_range:
                if self.check_valid_LOS_coordinate(current_x, tmp_y):
                    return (current_x, tmp_y)
            return None

        # Horizontal line:
        y_lower = get_valid_horizontal_coords(reversed(range(0, current_y)))
        y_upper = get_valid_horizontal_coords(range(current_y + 1, self.width_max))
        return [coords for coords in [y_lower, y_upper] if coords is not None]  # None = no seats in that line of sight

    def diagonal_fields_in_sight(self):
        """Gets the coordinates of any seats in the diagonal line of sight"""
        current_x, current_y = self.current_field

        def get_valid_diagonal_coords(x_lst, y_lst) -> tuple or None:
            """Cast to list due to range iterator object by reversed.
            Returns the first valid coordinate it comes across"""
            x_lst, y_lst = list(x_lst), list(y_lst)
            max_index = min(len(x_lst), len(y_lst))
            for i in range(0, max_index):
                cur_x, cur_y = x_lst[i], y_lst[i]
                if self.check_valid_LOS_coordinate(cur_x, cur_y):
                    return (cur_x, cur_y)
            return None
            # diagonals, go through the range quadrants:
        lower_y = list(reversed(range(0, current_y)))  # cast generator to list to preserve values
        upper_y = range(current_y + 1, self.width_max)
        lower_x = list(reversed(range(0, current_x)))  # cast generator to list to preserve values
        upper_x = range(current_x + 1, self.length_max)
        diags = [get_valid_diagonal_coords(x_l, y_l) for x_l, y_l
                 in [(lower_x, lower_y),  # To upper left corner
                     (upper_x, lower_y),  # To lower left corner
                     (upper_x, upper_y),  # To lower right corner
                     (lower_x, upper_y)]]  # To upper right corner

        return [coords for coords in diags if coords is not None]  # None = no seats in that line of sight

    def count_alive(self):
        """Count alive cells (filled seats) in the total matrix"""
        self.alive_cells = sum([sum([1 for seat in row if seat == STATE.alive]) for row in self.matrix])
