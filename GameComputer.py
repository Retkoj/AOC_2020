from copy import deepcopy
from enum import Enum
import re
from typing import List


class GameStatus(Enum):
    not_started = "The game hasn't started yet"
    running = "The game is running"
    finished_successfully = "The game finished successfully"
    finished_unsuccessfully = "The game quit with an error"


class GameComputer:
    def __init__(self, raw_input: List):
        self.commands = {}
        self.accumulator = 0
        self.index = 0
        self.current_value = 0
        self.score = 0
        self.number_of_commands = len(raw_input)
        self.status = GameStatus.not_started
        self.valid_moves = {
            "nop": self.nop_move,
            "jmp": self.jmp_move,
            "acc": self.acc_move
        }
        self.process_raw_input(raw_input)

    def process_raw_input(self, raw_input: List):
        """
        Processes list of raw input strings into self.commands dictionary.
        Commands are enumerated and expected to be of form "ccc dn+", i.e. 3 command characters, followed by a white
        space, a direction sign (+ or -) and a value of 1 or more numbers.
        e.g.
            ["jmp +227", "nop -8", "acc +21"]
        becomes:
        {
            1: {"action": "jmp", "value": 227},
            2: {"action": "nop", "value": -8}
            2: {"action": "acc", "value": 21}
        }
        """
        for i, command in enumerate(raw_input):
            parsed_command = re.findall(r'([a-z]{3}) ([\+|-][0-9]+)', command)
            if parsed_command:
                action, value = parsed_command[0]
                if action not in list(self.valid_moves.keys()):
                    raise NotImplementedError(f"Action {action} is not implemented")
                self.commands[i] = {
                    "action": action,
                    "value": int(value)
                }

    def run_game(self):
        """
        While self.index is still within the range of the game input, execute commands.
        If the same index is passed for a second time, the game quits to prevent infinite loops.
        When the game is done, save accumulator value to self.score and print game status
        """
        valid_index_range = list(range(0, self.number_of_commands))
        already_passed_indexes = []
        self.status = GameStatus.running
        self.print_game_status()
        while self.index in valid_index_range:  # prevent infinite loop
            if self.index in already_passed_indexes:
                self.status = GameStatus.finished_unsuccessfully
                break
            already_passed_indexes.append(self.index)
            self.make_move()
        self.score = self.accumulator
        if self.status == GameStatus.running:
            self.status = GameStatus.finished_successfully
        self.print_game_status()

    def reset_game(self):
        """Resets the games' variables"""
        self.accumulator = 0
        self.index = 0
        self.current_value = 0
        self.score = 0
        self.status = GameStatus.not_started

    def print_score(self):
        print(f'Score: {self.score}')

    def print_game_status(self):
        print(f'Game status: {self.status.value}')

    def set_commands(self, new_commands: dict):
        """Brute force set commands dict, useful in day 8_2"""
        self.commands = deepcopy(new_commands)

    def make_move(self):
        """Call the function for the current action"""
        action, self.current_value = self.commands[self.index].values()
        self.valid_moves[action]()

    def nop_move(self):
        """nop stands for No OPeration - it does nothing. The instruction immediately below it is executed next."""
        self.index += 1

    def jmp_move(self):
        """jmp jumps to a new instruction relative to itself. The next instruction to execute is found using the
        argument as an offset from the jmp instruction; for example, jmp +2 would skip the next instruction"""
        self.index += self.current_value

    def acc_move(self):
        """acc increases or decreases a single global value called the accumulator by the value given in the argument.
        For example, acc +7 would increase the accumulator by 7. The accumulator starts at 0. After an acc instruction,
        the instruction immediately below it is executed next."""
        self.accumulator += self.current_value
        self.index += 1
