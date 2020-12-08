import fileinput


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


def play_game(game_input: dict):
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
    return accumulator_at_2nd_run


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


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
    acc_value = play_game(output)
    print(f'Accumulator: {acc_value}')
