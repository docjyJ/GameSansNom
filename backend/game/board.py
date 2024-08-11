from enum import IntEnum

import numpy as np


class CaseState(IntEnum):
    """
    Enumeration for different game case states.

    Table of data format:
    |       | FALSE          | TRUE          |
    |------ |----------------|---------------|
    | BIT_2 | FREE           | PLAYED        |
    | BIT_1 | BLACK or EMPTY | PINK or TOTEM |
    | BIT_0 | CIRCLE         | CROSS         |
    """
    EMPTY        = 0b000
    UNUSED       = 0b001
    TOTEM_CIRCLE = 0b010
    TOTEM_CROSS  = 0b011
    BLACK_CIRCLE = 0b100
    BLACK_CROSS  = 0b101
    PINK_CIRCLE  = 0b110
    PINK_CROSS   = 0b111

class Players(IntEnum):
    """
    Enumeration for different player.
    """
    BLACK = 0
    PINK  = 1

class Board:
    def __init__(self):
        self.board = np.zeros((6, 6), dtype=np.uint8)
        self.board[2,2] = CaseState.TOTEM_CIRCLE
        self.board[3,3] = CaseState.TOTEM_CROSS
        self.turn = Players.BLACK
