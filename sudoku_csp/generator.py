# -*- coding: utf-8 -*-
"""Generate sudoku puzzles.

"""
import requests
from enum import Enum

import numpy as np


class SudokuDifficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    RANDOM = "random"


class Generator:

    generator_url = "https://sugoku.herokuapp.com/board"

    @classmethod
    def generate(
        cls, size: int = 3, difficulty: SudokuDifficulty = SudokuDifficulty.MEDIUM
    ):
        if size != 3:
            raise NotImplementedError(
                "Sudoku of size different than 3x3 are not currently supported."
            )

        params = {"difficulty": difficulty.value}
        response = requests.get(cls.generator_url, params=params)
        return np.array(response.json()["board"])
