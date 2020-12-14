import fileinput
import re
from typing import List


class DockingProgram:
    def __init__(self):
        self.memory = {key: 0 for key in range(0, 36)}
        self.mask = 'x' * 36
        self.mask_dict = {}

    def set_mask(self, mask: str):
        self.mask = mask
        self.mask_dict = {index: mask for index, mask in enumerate(list(mask)) if mask != 'X'}

    def set_value(self, memory_loc, new_memory_value):
        bin_value = format(new_memory_value, '036b')
        masked_val = self.process_value(bin_value)
        self.memory[memory_loc] = masked_val

    def process_value(self, value: str):
        value_as_list = list(value)
        for index, mask in self.mask_dict.items():
            value_as_list[index] = mask
        return int(''.join(value_as_list), 2)

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
            docking_computer.set_value(int(memory_loc), int(value))

    return docking_computer.memory_sum()


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
