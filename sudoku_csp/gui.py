"""
Application related GUI.
"""
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow
)


class MainWindow(QMainWindow):
    """
    A class to represent the app main window.
    """

    def __init__(self, title: str):
        """
        Constructs all the necessary attributes for the main window object.
        """
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("./sudoku_csp/assets/icon.jpg"))
