import fileinput
import re
from copy import deepcopy
from typing import List
import numpy as np


def all_permutations(length: int):
    values = [0, 1]
    all_combinations = []
    number_of_combinations = 2**length
    for i in range(1, length + 1):
        rep = 2**i / 2
        new_values = np.repeat(values, rep)
        new_values = np.tile(new_values, int(int(number_of_combinations / rep)/2))
        all_combinations.append(new_values)
    return all_combinations


def get_permutation(index, permutations):
    permutation = []
    for i in range(0, len(permutations)):
        permutation.append(permutations[i][index])
    return permutation


class DockingProgram:
    def __init__(self):
        self.memory = {key: 0 for key in range(0, 36)}
        self.mask = 'x' * 36
        self.mask_dict = {}
        self.memory_mask_dict = {}

    def set_mask(self, mask: str):
        self.mask = mask
        self.mask_dict = {index: mask for index, mask in enumerate(list(mask))}

    def set_value(self, memory_loc, new_memory_value):
        bin_value = format(new_memory_value, '036b')
        masked_val = self.process_value(bin_value)
        self.memory[memory_loc] = masked_val

    def process_value(self, value: str):
        value_as_list = list(value)
        for index, mask in self.mask_dict.items():
            if mask != 'X':
                value_as_list[index] = mask
        return int(''.join(value_as_list), 2)

    def set_value_to_multiple_memory_loc(self, memory_loc: int, new_memory_value: int):
        bin_value = format(memory_loc, '036b')
        all_memory_loc = self.process_memory_loc(bin_value)
        for loc in all_memory_loc:
            self.memory[loc] = new_memory_value

    def process_memory_loc(self, memory_loc: str):
        base_loc = list(memory_loc)
        for index, mask in self.mask_dict.items():
            if mask == '1':
                base_loc[index] = '1'

        num_floats = self.mask.count('X')
        float_permutations = all_permutations(num_floats)
        all_memory_locations = []
        for p in range(0, 2**num_floats):
            permutation = get_permutation(p, float_permutations)
            p_index = 0
            current_mem = deepcopy(base_loc)
            for index, mask in self.mask_dict.items():
                if mask == 'X':
                    current_mem[index] = str(permutation[p_index])
                    p_index += 1
            all_memory_locations.append(int(''.join(current_mem), 2))
        return all_memory_locations

    def memory_sum(self):
        return sum([value for value in self.memory.values()])


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
    docking_computer = DockingProgram()
    for command in input_list:
        command = command.split(' = ')
        goal = command[0]
        value = command[1]
        if goal == 'mask':
            docking_computer.set_mask(value)
        else:
            memory_loc = re.match(r'mem\[([0-9]+)\]', goal).groups()[0]
            docking_computer.set_value_to_multiple_memory_loc(int(memory_loc), int(value))

    return docking_computer.memory_sum()


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
