"""
Main application program.
"""
import sys

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication
import numpy as np

from sudoku_csp.gui import MainWindow
from sudoku_csp.interfaces import AlgorithmType, Resolver


class SudokuResolver(Resolver):
    """
    A worker who manage the resolving of the sudoku.
    """

    result_ready = Signal((AlgorithmType, np.ndarray))

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
        self.result_ready.emit(algorithm_type, sudoku_map)


if __name__ == "__main__":
    app = QApplication([])

    sudoku_solver = SudokuResolver()
    main_window = MainWindow("Sudoku solver", sudoku_solver)
    main_window.resize(1000, 600)
    main_window.show()

    sys.exit(app.exec())
