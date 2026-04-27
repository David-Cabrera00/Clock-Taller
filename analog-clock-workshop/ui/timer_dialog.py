from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class TimerDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Temporizador")
        self.setModal(False)
        self.resize(420, 320)
        self.setMinimumSize(380, 280)

        self.remaining_seconds = 0
        self.timer_running = False

        self.title_label = QLabel("Temporizador")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.minutes_input = QSpinBox()
        self.minutes_input.setRange(0, 180)
        self.minutes_input.setSuffix(" min")

        self.seconds_input = QSpinBox()
        self.seconds_input.setRange(0, 59)
        self.seconds_input.setSuffix(" s")

        self.time_label = QLabel("00:00")
        self.time_label.setObjectName("timeLabel")
        self.time_label.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel("Configure el tiempo y presione iniciar.")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Iniciar")
        self.pause_button = QPushButton("Pausar")
        self.reset_button = QPushButton("Reiniciar")

        self._build_ui()
        self._apply_styles()
        self._connect_events()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.setInterval(1000)

    def _build_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(22, 20, 22, 20)
        root_layout.setSpacing(16)

        root_layout.addWidget(self.title_label)

        inputs_row = QHBoxLayout()
        inputs_row.setSpacing(10)

        minutes_container = self._create_input_box("Minutos", self.minutes_input)
        seconds_container = self._create_input_box("Segundos", self.seconds_input)

        inputs_row.addWidget(minutes_container)
        inputs_row.addWidget(seconds_container)

        buttons_row = QHBoxLayout()
        buttons_row.setSpacing(10)
        buttons_row.addWidget(self.start_button)
        buttons_row.addWidget(self.pause_button)
        buttons_row.addWidget(self.reset_button)

        root_layout.addLayout(inputs_row)
        root_layout.addWidget(self.time_label)
        root_layout.addWidget(self.status_label)
        root_layout.addLayout(buttons_row)

    def _create_input_box(self, title: str, widget: QWidget) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        label = QLabel(title)
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("fieldLabel")

        layout.addWidget(label)
        layout.addWidget(widget)

        return container

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QDialog {
                background-color: #0c101d;
            }

            QLabel {
                color: #f3efff;
                background: transparent;
            }

            QLabel#titleLabel {
                font-size: 22px;
                font-weight: 900;
                color: #ff87a0;
            }

            QLabel#fieldLabel {
                font-size: 13px;
                font-weight: 700;
                color: #d4c8ef;
            }

            QLabel#timeLabel {
                font-size: 48px;
                font-weight: 900;
                color: #f5f1ff;
                padding-top: 8px;
                padding-bottom: 4px;
            }

            QLabel#statusLabel {
                font-size: 13px;
                font-weight: 700;
                color: #ffd0d8;
                padding-bottom: 4px;
            }

            QSpinBox {
                background-color: #141b2c;
                color: #f2eeff;
                border: 1px solid rgba(199, 120, 255, 0.22);
                border-radius: 12px;
                padding: 10px;
                font-size: 15px;
                font-weight: 700;
                min-height: 24px;
            }

            QPushButton {
                background-color: #171f33;
                color: #f2eeff;
                border: 1px solid rgba(199, 120, 255, 0.20);
                border-radius: 14px;
                padding: 10px 16px;
                font-size: 14px;
                font-weight: 800;
            }

            QPushButton:hover {
                background-color: #1f2942;
                border: 1px solid rgba(255, 122, 150, 0.38);
            }
            """
        )

    def _connect_events(self) -> None:
        self.start_button.clicked.connect(self._start_countdown)
        self.pause_button.clicked.connect(self._pause_countdown)
        self.reset_button.clicked.connect(self._reset_countdown)

    def _start_countdown(self) -> None:
        if not self.timer_running:
            if self.remaining_seconds <= 0:
                total_seconds = (
                    self.minutes_input.value() * 60 + self.seconds_input.value()
                )

                if total_seconds <= 0:
                    self.status_label.setText("Ingrese un tiempo mayor que cero.")
                    return

                self.remaining_seconds = total_seconds

            self.timer.start()
            self.timer_running = True
            self.status_label.setText("Temporizador en ejecución.")
            self._update_time_label()

    def _pause_countdown(self) -> None:
        if self.timer_running:
            self.timer.stop()
            self.timer_running = False
            self.status_label.setText("Temporizador en pausa.")

    def _reset_countdown(self) -> None:
        self.timer.stop()
        self.timer_running = False
        self.remaining_seconds = 0
        self.time_label.setText("00:00")
        self.status_label.setText("Temporizador reiniciado.")

    def _tick(self) -> None:
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self._update_time_label()

        if self.remaining_seconds <= 0:
            self.timer.stop()
            self.timer_running = False
            self.time_label.setText("00:00")
            self.status_label.setText("Tiempo finalizado.")
            QApplication.beep()

    def _update_time_label(self) -> None:
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")
