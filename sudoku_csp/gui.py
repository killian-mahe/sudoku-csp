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
    QMenu,
)
import numpy as np

from generator import Generator, SudokuDifficulty
from interfaces import AlgorithmType


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

        self.generate_menu = QMenu("Generate", self)
        self.solve_menu = QMenu("Solve", self)

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

        generate_easy_action = QAction("Easy", self)
        generate_easy_action.setShortcut("Ctrl+E")
        generate_easy_action.setCheckable(False)
        generate_easy_action.triggered.connect(
            lambda x: self.handle_generation(SudokuDifficulty.EASY)
        )

        generate_medium_action = QAction("Medium", self)
        generate_medium_action.setShortcut("Ctrl+M")
        generate_medium_action.setCheckable(False)
        generate_medium_action.triggered.connect(
            lambda x: self.handle_generation(SudokuDifficulty.MEDIUM)
        )

        generate_hard_action = QAction("Hard", self)
        generate_hard_action.setShortcut("Ctrl+H")
        generate_hard_action.setCheckable(False)
        generate_hard_action.triggered.connect(
            lambda x: self.handle_generation(SudokuDifficulty.HARD)
        )

        generate_random_action = QAction("Random", self)
        generate_random_action.setShortcut("Ctrl+R")
        generate_random_action.setCheckable(False)
        generate_random_action.triggered.connect(
            lambda x: self.handle_generation(SudokuDifficulty.RANDOM)
        )

        self.generate_menu.addActions(
            [
                generate_easy_action,
                generate_medium_action,
                generate_hard_action,
                generate_random_action,
            ]
        )
        self.menuBar().addMenu(self.generate_menu)

        solve_backtracking_action = QAction("Backtracking", self)
        solve_backtracking_action.triggered.connect(
            lambda x: self.handle_resolve(AlgorithmType.BACKTRACKING)
        )

        solve_mrv_action = QAction("MRV", self)
        solve_mrv_action.triggered.connect(
            lambda x: self.handle_resolve(AlgorithmType.MRV)
        )

        solve_ac3_action = QAction("AC-3", self)
        solve_ac3_action.triggered.connect(
            lambda x: self.handle_resolve(AlgorithmType.AC3)
        )

        solve_degree_h_action = QAction("Degree heuristic", self)
        solve_degree_h_action.triggered.connect(
            lambda x: self.handle_resolve(AlgorithmType.DEGREE_H)
        )

        solve_least_constraining_h_action = QAction("Least constraining value", self)
        solve_least_constraining_h_action.triggered.connect(
            lambda x: self.handle_resolve(AlgorithmType.LEAST_CONSTRAINING_H)
        )

        self.solve_menu.addActions(
            [
                solve_backtracking_action,
                solve_mrv_action,
                solve_ac3_action,
                solve_degree_h_action,
                solve_least_constraining_h_action
            ]
        )
        self.solve_menu.setEnabled(False)
        self.menuBar().addMenu(self.solve_menu)

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

    def handle_generation(self, difficulty: SudokuDifficulty = SudokuDifficulty.EASY):
        self.digits_map = Generator.generate(self.size, difficulty)

        for y in range(self.size):
            for x in range(self.size):

                self.clear_cell([x, y])

                if self.digits_map[x, y] != 0:
                    self.draw_number(self.digits_map[x, y], np.array([x, y]))

        self.solve_menu.setEnabled(True)

    def handle_resolve(self, algorithm_type: AlgorithmType):
        print(f"Trying to resolve using {algorithm_type.value} algorithm")
        self.solve_menu.setEnabled(False)
