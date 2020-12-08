import fileinput
from copy import deepcopy

from GameComputer import GameComputer, GameStatus


def find_change(game: GameComputer):
    """
    Find accumulator value when the infinite loop is broken by changing 1 jmp to nop or 1 nop to jmp.

    Loops through all indexes of the game-loop and tries to change the actions one at a time.
    Prints accumulator value when a change was effective.

    :param game: GameComputer object
    """
    original_dict = deepcopy(game.commands)
    for index in range(0, game.number_of_commands):
        tmp_dict = deepcopy(original_dict)
        if tmp_dict[index]['action'] == 'jmp':
            tmp_dict[index]['action'] = 'nop'
        elif tmp_dict[index]['action'] == 'nop':
            tmp_dict[index]['action'] = 'jmp'
        game.reset_game()
        game.set_commands(tmp_dict)
        game.run_game()
        if game.status == GameStatus.finished_successfully:
            game.print_score()
            break


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    game_computer = GameComputer(lines)
    find_change(game_computer)
