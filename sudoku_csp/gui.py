"""
Application related GUI.
"""
from PySide6 import QtWidgets
from PySide6.QtCore import QRectF, QPointF
from PySide6.QtGui import QIcon, QAction, QFont, QPainter, QPen
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


from generator import Generator


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
        self.cell_width = 500 / self.size
        self.box_map: np.array = np.empty((self.size, self.size, 2), dtype=object)
        self.digits_map: np.array = np.zeros((self.size, self.size))

        self.setCentralWidget(QtWidgets.QWidget())
        self.centralWidget().setLayout(self.layout)

        self.create_menus()
        self.create_sudoku_view(self.size)

    def create_sudoku_view(self, n: int = 9):
        self.layout.addWidget(self.sudoku_view)

        for y in range(0, n):
            for x in range(0, n):
                self.box_map[x, y] = [
                    self.sudoku_scene.addRect(
                        QRectF(
                            self.cell_width * x,
                            self.cell_width * y,
                            self.cell_width,
                            self.cell_width,
                        )
                    ),
                    None,
                ]

        # Draw visual lines
        if n == 9:
            pen = QPen()
            pen.setWidth(3)
            for i in range(1, 3):
                self.sudoku_scene.addLine(
                    i * 3 * self.cell_width,
                    0,
                    i * 3 * self.cell_width,
                    n * self.cell_width,
                    pen,
                )
                self.sudoku_scene.addLine(
                    0,
                    i * 3 * self.cell_width,
                    n * self.cell_width,
                    i * 3 * self.cell_width,
                    pen,
                )

    def create_menus(self):
        self.setMenuBar(QMenuBar())

        import_action = QAction("Import", self)
        import_action.setShortcut("Ctrl+I")
        import_action.triggered.connect(self.handle_import)
        import_action.setEnabled(False)
        self.menuBar().addAction(import_action)

        generate_action = QAction("Generate", self)
        generate_action.setShortcut("Ctrl+N")
        generate_action.triggered.connect(self.handle_generation)
        self.menuBar().addAction(generate_action)

        self.setStatusBar(QStatusBar())

    def draw_number(self, number: int, pos: np.array, size: int = 30):
        text = DigitText()
        self.box_map[pos[0], pos[1], 1] = text

        text.setFont(QFont("Arial", size, QFont.Bold))
        text.setText(str(number))

        pos = pos * self.cell_width + self.cell_width / 2
        text.setPos(QPointF(pos[0], pos[1]))
        self.sudoku_scene.addItem(text)
        return text

    def clear_cell(self, pos: np.array):
        self.sudoku_scene.removeItem(self.box_map[pos[0], pos[1], 1])
        self.box_map[pos[0], pos[1], 1] = None

    def handle_import(self):
        pass

    def handle_generation(self):
        self.digits_map = Generator.generate(self.size)

        for y in range(self.size):
            for x in range(self.size):

                self.clear_cell([x, y])

                if self.digits_map[x, y] != 0:
                    self.draw_number(self.digits_map[x, y], np.array([x, y]))
