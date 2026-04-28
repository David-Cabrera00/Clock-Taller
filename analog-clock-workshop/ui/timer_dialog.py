import winsound

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
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

        self.resize(460, 360)
        self.setMinimumSize(430, 340)

        self.remaining_seconds = 0
        self.timer_running = False
        self.theme_name = "Rose"

        self.themes = {
            "Rose": {
                "background": "#0a0d18",
                "card": "#101525",
                "card_soft": "#141b2f",
                "title": "#ff8ea6",
                "text": "#f5f1ff",
                "muted": "#d8ccec",
                "status": "#ffb8c6",
                "input_bg": "#1a2238",
                "input_border": "rgba(199, 120, 255, 0.22)",
                "button_bg": "#1a233a",
                "button_hover": "#243150",
                "button_border": "rgba(199, 120, 255, 0.20)",
                "button_hover_border": "rgba(255, 122, 150, 0.42)",
            },
            "Emerald": {
                "background": "#08120f",
                "card": "#0f1b18",
                "card_soft": "#132521",
                "title": "#64e5c4",
                "text": "#effff9",
                "muted": "#c9eee3",
                "status": "#b6f1e0",
                "input_bg": "#1a2d29",
                "input_border": "rgba(76, 224, 186, 0.24)",
                "button_bg": "#18302b",
                "button_hover": "#21423b",
                "button_border": "rgba(76, 224, 186, 0.22)",
                "button_hover_border": "rgba(76, 224, 186, 0.42)",
            },
            "Gold": {
                "background": "#16110a",
                "card": "#1b140d",
                "card_soft": "#241b11",
                "title": "#f2c14e",
                "text": "#fff7e8",
                "muted": "#f0dfb4",
                "status": "#ffe1a3",
                "input_bg": "#302317",
                "input_border": "rgba(242, 193, 78, 0.24)",
                "button_bg": "#322416",
                "button_hover": "#43301d",
                "button_border": "rgba(242, 193, 78, 0.22)",
                "button_hover_border": "rgba(242, 193, 78, 0.42)",
            },
        }

        self.title_label = QLabel("Temporizador")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.subtitle_label = QLabel("Configure minutos y segundos")
        self.subtitle_label.setObjectName("subtitleLabel")
        self.subtitle_label.setAlignment(Qt.AlignCenter)

        self.minutes_label = QLabel("Minutos")
        self.minutes_label.setObjectName("fieldLabel")
        self.minutes_label.setAlignment(Qt.AlignCenter)

        self.seconds_label = QLabel("Segundos")
        self.seconds_label.setObjectName("fieldLabel")
        self.seconds_label.setAlignment(Qt.AlignCenter)

        self.minutes_input = QSpinBox()
        self.minutes_input.setRange(0, 180)
        self.minutes_input.setSuffix(" min")
        self.minutes_input.setAlignment(Qt.AlignCenter)

        self.seconds_input = QSpinBox()
        self.seconds_input.setRange(0, 59)
        self.seconds_input.setSuffix(" s")
        self.seconds_input.setAlignment(Qt.AlignCenter)

        self.time_label = QLabel("00:00")
        self.time_label.setObjectName("timeLabel")
        self.time_label.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel("Configure el tiempo y presione iniciar.")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)

        self.start_button = QPushButton("Iniciar")
        self.start_button.setObjectName("actionButton")

        self.pause_button = QPushButton("Pausar")
        self.pause_button.setObjectName("actionButton")

        self.reset_button = QPushButton("Reiniciar")
        self.reset_button.setObjectName("actionButton")

        self._build_ui()
        self._apply_styles()
        self._connect_events()
        self._update_button_states()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.setInterval(1000)

    def set_theme(self, theme_name: str) -> None:
        if theme_name in self.themes:
            self.theme_name = theme_name
            self._apply_styles()

    def _build_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(14)

        root_layout.addWidget(self.title_label)
        root_layout.addWidget(self.subtitle_label)

        inputs_card = QFrame()
        inputs_card.setObjectName("card")
        inputs_layout = QGridLayout(inputs_card)
        inputs_layout.setContentsMargins(16, 16, 16, 16)
        inputs_layout.setHorizontalSpacing(14)
        inputs_layout.setVerticalSpacing(8)

        inputs_layout.addWidget(self.minutes_label, 0, 0)
        inputs_layout.addWidget(self.seconds_label, 0, 1)
        inputs_layout.addWidget(self.minutes_input, 1, 0)
        inputs_layout.addWidget(self.seconds_input, 1, 1)

        display_card = QFrame()
        display_card.setObjectName("displayCard")
        display_layout = QVBoxLayout(display_card)
        display_layout.setContentsMargins(18, 18, 18, 18)
        display_layout.setSpacing(8)
        display_layout.addWidget(self.time_label)
        display_layout.addWidget(self.status_label)

        buttons_card = QFrame()
        buttons_card.setObjectName("card")
        buttons_layout = QHBoxLayout(buttons_card)
        buttons_layout.setContentsMargins(14, 12, 14, 12)
        buttons_layout.setSpacing(8)
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.pause_button)
        buttons_layout.addWidget(self.reset_button)

        root_layout.addWidget(inputs_card)
        root_layout.addWidget(display_card)
        root_layout.addWidget(buttons_card)

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
                font-size: 28px;
                font-weight: 900;
                color: {palette["title"]};
                padding-top: 4px;
            }}

            QLabel#subtitleLabel {{
                font-size: 13px;
                font-weight: 600;
                color: {palette["muted"]};
                padding-bottom: 2px;
            }}

            QLabel#fieldLabel {{
                font-size: 14px;
                font-weight: 800;
                color: {palette["muted"]};
            }}

            QLabel#timeLabel {{
                font-size: 52px;
                font-weight: 900;
                color: {palette["text"]};
                padding-top: 4px;
            }}

            QLabel#statusLabel {{
                font-size: 13px;
                font-weight: 700;
                color: {palette["status"]};
            }}

            QFrame#card {{
                background-color: {palette["card"]};
                border: 1px solid {palette["button_border"]};
                border-radius: 18px;
            }}

            QFrame#displayCard {{
                background-color: {palette["card_soft"]};
                border: 1px solid {palette["button_border"]};
                border-radius: 20px;
            }}

            QSpinBox {{
                background-color: {palette["input_bg"]};
                color: {palette["text"]};
                border: 1px solid {palette["input_border"]};
                border-radius: 12px;
                padding: 10px;
                font-size: 18px;
                font-weight: 800;
                min-height: 24px;
            }}

            QPushButton#actionButton {{
                background-color: {palette["button_bg"]};
                color: {palette["text"]};
                border: 1px solid {palette["button_border"]};
                border-radius: 12px;
                padding: 8px 12px;
                font-size: 14px;
                font-weight: 800;
                min-width: 88px;
                max-width: 110px;
                min-height: 18px;
            }}

            QPushButton#actionButton:hover {{
                background-color: {palette["button_hover"]};
                border: 1px solid {palette["button_hover_border"]};
            }}

            QPushButton#actionButton:disabled {{
                background-color: rgba(90, 90, 90, 0.18);
                color: rgba(255, 255, 255, 0.35);
                border: 1px solid rgba(255, 255, 255, 0.08);
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
                    self._update_button_states()
                    return

                self.remaining_seconds = total_seconds

            self.timer.start()
            self.timer_running = True
            self.status_label.setText("Temporizador en ejecución.")
            self._update_time_label()
            self._update_button_states()

    def _pause_countdown(self) -> None:
        if self.timer_running:
            self.timer.stop()
            self.timer_running = False
            self.status_label.setText("Temporizador en pausa.")
            self._update_button_states()

    def _reset_countdown(self) -> None:
        self.timer.stop()
        self.timer_running = False
        self.remaining_seconds = 0
        self.time_label.setText("00:00")
        self.status_label.setText("Temporizador reiniciado.")
        self._update_button_states()

    def _tick(self) -> None:
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self._update_time_label()

        if self.remaining_seconds <= 0:
            self.timer.stop()
            self.timer_running = False
            self.time_label.setText("00:00")
            self.status_label.setText("Tiempo finalizado.")
            self._play_finish_sound()
            self._update_button_states()

    def _update_time_label(self) -> None:
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")

    def _update_button_states(self) -> None:
        self.pause_button.setEnabled(self.timer_running)
        self.reset_button.setEnabled(self.timer_running or self.remaining_seconds > 0)

    def _play_finish_sound(self) -> None:
        try:
            winsound.Beep(1200, 250)
            winsound.Beep(1000, 250)
            winsound.Beep(1400, 350)
        except Exception:
            QApplication.beep()

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)

        if self.parent() is not None:
            parent_geometry = self.parent().geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            self.move(max(x, 0), max(y, 0))