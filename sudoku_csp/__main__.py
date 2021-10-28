"""
Main application program.
"""
import traceback
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Signal
import numpy as np

from sudoku_csp.interfaces import AlgorithmType, Resolver
from sudoku_csp.gui import MainWindow
from sudoku_csp.csp import SudokuCSP


class SudokuResolver(Resolver):
    """
    A worker who manage the resolving of the sudoku.
    """

    result_ready = Signal((AlgorithmType, np.ndarray))
    error = Signal(str)

    def do_work(
        self,
        algorithm_type: AlgorithmType = AlgorithmType.BACKTRACKING,
        sudoku_map: np.array = np.array([]),
    ):
        """
        Do the asked work using the choosen algorithm.

        Parameters
        ----------
        algorithm_type : AlgorithmType
            A type of algorithm to user to resolve the sudoku.
        sudoku_map : np.array
            A array containing the map of the sudoku.

        Returns
        -------
        None
        """
        try:
            csp = SudokuCSP(sudoku_map)

            if algorithm_type == AlgorithmType.BACKTRACKING:
                pass
            elif algorithm_type == AlgorithmType.MRV:
                pass
            elif algorithm_type == AlgorithmType.DEGREE_H:
                pass
            elif algorithm_type == AlgorithmType.LEAST_CONSTRAINING_H:
                pass
            elif algorithm_type == AlgorithmType.AC3:
                pass
        except Exception:
            print(traceback.format_exc())
            self.error.emit(traceback.format_exc())
        self.result_ready.emit(algorithm_type, sudoku_map)


if __name__ == "__main__":
    app = QApplication([])

    sudoku_solver = SudokuResolver()
    main_window = MainWindow("Sudoku solver", sudoku_solver)
    main_window.resize(1000, 600)
    main_window.show()

    sys.exit(app.exec())
