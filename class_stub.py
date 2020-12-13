from copy import deepcopy
from enum import Enum
import re
from typing import List


class SomeEnum(Enum):
    pass


class SomeClass:
    def __init__(self, raw_input: List):
        self.input = raw_input
        self.process_input()

    def process_input(self):
        pass