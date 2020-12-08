import fileinput
from pathlib import Path
from copy import deepcopy


def make_move(command, index, accumulator):
    action, direction, value = command.values()
    if action == 'nop':
        return index + 1, accumulator
    if action == 'jmp':
        index = index + value if direction == '+' else index - value
        return index, accumulator
    if action == 'acc':
        accumulator = accumulator + value if direction == '+' else accumulator - value
        return index + 1, accumulator


def find_original_game_loop(game_input: dict):
    passed_index = []
    accumulator = 0
    second_run = False
    index = 0
    accumulator_at_2nd_run = None
    while not second_run:
        if index in passed_index:
            accumulator_at_2nd_run = accumulator
            second_run = True
        else:
            passed_index.append(index)
            index, accumulator = make_move(game_input[index], index, accumulator)
    return accumulator_at_2nd_run, passed_index


def play_game_infinite(game_input: dict):
    """
    Plays the game until the index is out of bounds or until the game is in a loop

    :param game_input:
    :return:
    """
    passed_index = []
    accumulator = 0
    index = 0
    index_range = list(range(0, len(game_input)))
    while index in index_range:
        if index in passed_index:
            return None
        passed_index.append(index)
        index, accumulator = make_move(game_input[index], index, accumulator)
    return accumulator


def process(input_list: list) -> dict:
    """

    :param input_list:
    :return:
    """
    input_dict = {}
    for i, command in enumerate(input_list):
        action = command.split(' ')[0]
        value_direction = command.split(' ')[1][0]
        value = command.split(' ')[1][1:]
        input_dict[i] = {
            "action": action,
            "direction": value_direction,
            "value": int(value)
        }
    return input_dict


def write_indexes_to_file(original_lines, passed_indexes):
    file_path = Path().cwd() / 'data' / 'tmp.txt'
    with open(str(file_path), 'w+') as f:
        # passed_indexes.sort()
        for i in passed_indexes:
            f.write(str(i) + ' ' + original_lines[i] + '\n')


def check_indexes(lines, game_dict):
    acc_value, indexes = find_original_game_loop(processed_lines)
    print(f'Accumulator: {acc_value}')
    write_indexes_to_file(lines, indexes)


def find_correct_change(original_dict):
    """
    Find accumulator value when the infinite loop is broken by changing 1 jmp to nop or 1 nop to jmp.

    Loops through the indexes of the original game-loop and tries to change the actions one at a time.
    Returns accumulator value when a change was effective.

    :param original_dict: Original game input dictionary
    :return: accumulator value or None
    """
    acc_value_orig, indexes_orig = find_original_game_loop(original_dict)
    for index in indexes_orig:
        tmp_dict = deepcopy(original_dict)
        if tmp_dict[index]['action'] == 'jmp':
            tmp_dict[index]['action'] = 'nop'
        elif tmp_dict[index]['action'] == 'nop':
            tmp_dict[index]['action'] = 'jmp'
        acc_value = play_game_infinite(tmp_dict)
        if acc_value:
            return acc_value
    return None


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    processed_lines = process(lines)
    print(f'Output: {processed_lines}')
    acc = find_correct_change(processed_lines)
    print(f'Found it! {acc}')



