"""
Application related GUI.
"""
from PySide6.QtWidgets import (
    QMainWindow
)


class MainWindow(QMainWindow):
    """
    A class to represent the app main window.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the main window object.
        """
        super().__init__()
