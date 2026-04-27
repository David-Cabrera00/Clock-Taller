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
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Temporizador")
        self.setModal(False)
        self.setWindowModality(Qt.NonModal)
        self.setWindowFlag(Qt.Window, True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.resize(420, 320)
        self.setMinimumSize(380, 280)

        self.remaining_seconds = 0
        self.timer_running = False
        self.theme_name = "Rose"

        self.themes = {
            "Rose": {
                "background": "#0c101d",
                "title": "#ff87a0",
                "text": "#f3efff",
                "muted": "#d4c8ef",
                "status": "#ffd0d8",
                "input_bg": "#141b2c",
                "input_border": "rgba(199, 120, 255, 0.22)",
                "button_bg": "#171f33",
                "button_hover": "#1f2942",
                "button_border": "rgba(199, 120, 255, 0.20)",
                "button_hover_border": "rgba(255, 122, 150, 0.38)",
            },
            "Emerald": {
                "background": "#0a1412",
                "title": "#62e8c5",
                "text": "#effff9",
                "muted": "#c6f0e4",
                "status": "#bdf7e6",
                "input_bg": "#12211e",
                "input_border": "rgba(76, 224, 186, 0.24)",
                "button_bg": "#162925",
                "button_hover": "#1c3732",
                "button_border": "rgba(76, 224, 186, 0.22)",
                "button_hover_border": "rgba(76, 224, 186, 0.42)",
            },
            "Gold": {
                "background": "#16110a",
                "title": "#f2c14e",
                "text": "#fff7e8",
                "muted": "#f1dfb4",
                "status": "#ffe0a0",
                "input_bg": "#241b12",
                "input_border": "rgba(242, 193, 78, 0.24)",
                "button_bg": "#2b2015",
                "button_hover": "#3a2a1a",
                "button_border": "rgba(242, 193, 78, 0.22)",
                "button_hover_border": "rgba(242, 193, 78, 0.42)",
            },
        }

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

    def set_theme(self, theme_name: str) -> None:
        if theme_name in self.themes:
            self.theme_name = theme_name
            self._apply_styles()

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
        palette = self.themes[self.theme_name]

        self.setStyleSheet(
            f"""
            QDialog {{
                background-color: {palette["background"]};
            }}

            QLabel {{
                color: {palette["text"]};
                background: transparent;
            }}

            QLabel#titleLabel {{
                font-size: 22px;
                font-weight: 900;
                color: {palette["title"]};
            }}

            QLabel#fieldLabel {{
                font-size: 13px;
                font-weight: 700;
                color: {palette["muted"]};
            }}

            QLabel#timeLabel {{
                font-size: 48px;
                font-weight: 900;
                color: {palette["text"]};
                padding-top: 8px;
                padding-bottom: 4px;
            }}

            QLabel#statusLabel {{
                font-size: 13px;
                font-weight: 700;
                color: {palette["status"]};
                padding-bottom: 4px;
            }}

            QSpinBox {{
                background-color: {palette["input_bg"]};
                color: {palette["text"]};
                border: 1px solid {palette["input_border"]};
                border-radius: 12px;
                padding: 10px;
                font-size: 15px;
                font-weight: 700;
                min-height: 24px;
            }}

            QPushButton {{
                background-color: {palette["button_bg"]};
                color: {palette["text"]};
                border: 1px solid {palette["button_border"]};
                border-radius: 14px;
                padding: 10px 16px;
                font-size: 14px;
                font-weight: 800;
            }}

            QPushButton:hover {{
                background-color: {palette["button_hover"]};
                border: 1px solid {palette["button_hover_border"]};
            }}
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