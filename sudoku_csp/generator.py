# -*- coding: utf-8 -*-
"""Generate sudoku puzzles.

"""
import random

from enum import Enum

import numpy as np


class SudokuDifficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Generator:
    @classmethod
    def generate(
        cls, size: int = 3, difficulty: SudokuDifficulty = SudokuDifficulty.MEDIUM
    ):

        if difficulty == SudokuDifficulty.EASY:
            difficulty = 0.5
        elif difficulty == SudokuDifficulty.MEDIUM:
            difficulty = 0.6
        elif difficulty == SudokuDifficulty.HARD:
            difficulty = 0.7

        sudoku_map = np.zeros((size ** 2, size ** 2), dtype=int)

        possible_values = set(np.arange(1, size ** 2 + 1))

        for y in range(size ** 2):
            for x in range(size ** 2):
                if random.random() > difficulty:

                    row = sudoku_map[y, :]
                    col = sudoku_map[:, x]

                    box = np.zeros((size, size), dtype=int)

                    for j in range(size):
                        for i in range(size):

                            x_box = size * int((x / size)) + i
                            y_box = size * int((y / size)) + j
                            box[j, i] = sudoku_map[y_box, x_box]

                    box = box.flatten()

                    assigned_values = np.concatenate((row, col, box))

                    unassigned_values = list(
                        possible_values.symmetric_difference(set(assigned_values))
                    )

                    index = random.randrange(len(unassigned_values))
                    sudoku_map[y, x] = unassigned_values[index]

        return sudoku_map
