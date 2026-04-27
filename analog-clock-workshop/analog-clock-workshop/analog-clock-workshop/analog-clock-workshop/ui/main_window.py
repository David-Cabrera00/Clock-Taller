from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QMainWindow, QVBoxLayout, QWidget

from ui.clock_face_widget import ClockFaceWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Reloj Analógico")
        self.resize(900, 900)
        self.setMinimumSize(700, 700)

        self.clock_widget = ClockFaceWidget()

        self._build_ui()
        self._apply_styles()

    def _build_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(30, 30, 30, 30)
        root_layout.setAlignment(Qt.AlignCenter)

        clock_card = QFrame()
        clock_card.setObjectName("clockCard")

        clock_layout = QVBoxLayout(clock_card)
        clock_layout.setContentsMargins(24, 24, 24, 24)
        clock_layout.setAlignment(Qt.AlignCenter)
        clock_layout.addWidget(self.clock_widget, alignment=Qt.AlignCenter)

        root_layout.addWidget(clock_card, alignment=Qt.AlignCenter)

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #edf1f5;
            }

            QFrame#clockCard {
                background-color: white;
                border: 1px solid #d5dde8;
                border-radius: 24px;
            }
            """
        )