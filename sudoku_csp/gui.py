"""
Application related GUI.
"""
from PySide6 import QtWidgets
from PySide6.QtCore import QRectF, QPointF
from PySide6.QtGui import QIcon, QAction, QFont, QPainter
from PySide6.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QStatusBar,
    QGridLayout,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsSimpleTextItem,
    QGraphicsItem,
    QStyleOptionGraphicsItem,
    QWidget,
)
import numpy as np


class DigitText(QGraphicsSimpleTextItem):
    def __init__(self, parent: QGraphicsItem = None):
        super().__init__(parent)

    def boundingRect(self):
        br = QGraphicsSimpleTextItem.boundingRect(self)
        return br.translated(-br.width() / 2, -br.height() / 2)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = 0
    ):
        painter.translate(
            -self.boundingRect().width() / 2, -self.boundingRect().height() / 2
        )
        QGraphicsSimpleTextItem.paint(self, painter, option, widget)


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

        self.layout = QGridLayout()
        self.sudoku_scene = QGraphicsScene()
        self.sudoku_view = QGraphicsView(self.sudoku_scene)

        self.size = 9
        self.box_map = np.empty((self.size, self.size, 2), dtype=object)
        self.digits_map = np.zeros((self.size, self.size))

        self.setCentralWidget(QtWidgets.QWidget())
        self.centralWidget().setLayout(self.layout)

        self.create_menus()
        self.create_sudoku_view(self.size)

    def create_sudoku_view(self, n: int = 9, width: int = 500):
        self.layout.addWidget(self.sudoku_view)

        box_width = width / n

        for y in range(0, n):
            for x in range(0, n):
                self.box_map[x, y] = [
                    self.sudoku_scene.addRect(
                        QRectF(box_width * x, box_width * y, box_width, box_width)
                    ),
                    None
                ]

    def create_menus(self):
        self.setMenuBar(QMenuBar())

        import_action = QAction("Import", self)
        import_action.setShortcut("Ctrl+I")
        import_action.triggered.connect(self.handle_import)
        self.menuBar().addAction(import_action)

        generate_action = QAction("Generate", self)
        generate_action.setShortcut("Ctrl+N")
        generate_action.triggered.connect(self.handle_generation)
        self.menuBar().addAction(generate_action)

        self.setStatusBar(QStatusBar())

    def draw_number(self, number: int, pos: tuple, size: int = 30):
        text = DigitText()
        text.setFont(QFont("Arial", size, QFont.Bold))
        text.setText(str(number))
        text.setPos(QPointF(pos[0], pos[1]))
        self.sudoku_scene.addItem(text)
        return text

    def handle_import(self):
        print("Importing a new sudoku")

    def handle_generation(self):
        print("Generating a new sudoku")
