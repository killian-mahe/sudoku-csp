"""
Main application program.
"""
import sys

from PySide6.QtWidgets import QApplication

from sudoku_csp.gui import MainWindow


if __name__ == "__main__":
    app = QApplication([])

    main_window = MainWindow("Sudoku solver")
    main_window.resize(1000, 600)
    main_window.show()

    sys.exit(app.exec())
