from datetime import datetime, timedelta, timezone

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from core.clock_city import ClockCity
from core.world_clock_cycle import WorldClockCycle
from ui.clock_face_widget import ClockFaceWidget
from ui.timer_dialog import TimerDialog


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Reloj Analógico")
        self.resize(1100, 900)
        self.setMinimumSize(860, 760)

        self.city_cycle = WorldClockCycle()
        self._load_cities()

        self.theme_order = ["Rose", "Emerald", "Gold"]
        self.theme_labels = {
            "Rose": "Rosa",
            "Emerald": "Esmeralda",
            "Gold": "Dorado",
        }
        self.current_theme_index = 0

        self.themes = {
            "Rose": {
                "background": "#060913",
                "card": "rgba(10, 13, 26, 0.78)",
                "selector": "rgba(10, 13, 26, 0.68)",
                "border": "rgba(199, 120, 255, 0.18)",
                "border_soft": "rgba(199, 120, 255, 0.14)",
                "title": "#ff8ca7",
                "top": "#f1d8ff",
                "text": "#f4f1ff",
                "muted": "#e7def8",
                "accent": "#ff6a83",
                "button": "rgba(17, 22, 38, 0.92)",
                "button_hover": "rgba(27, 34, 56, 0.96)",
                "button_checked_bg": "rgba(43, 19, 34, 0.96)",
                "button_checked_text": "#ff7e94",
                "button_checked_border": "#ff667f",
            },
            "Emerald": {
                "background": "#07120f",
                "card": "rgba(8, 20, 18, 0.80)",
                "selector": "rgba(8, 20, 18, 0.70)",
                "border": "rgba(76, 224, 186, 0.18)",
                "border_soft": "rgba(76, 224, 186, 0.14)",
                "title": "#69e8c9",
                "top": "#dbfff5",
                "text": "#f2fffb",
                "muted": "#d9f5ed",
                "accent": "#4ce0ba",
                "button": "rgba(13, 30, 27, 0.94)",
                "button_hover": "rgba(21, 43, 39, 0.98)",
                "button_checked_bg": "rgba(14, 44, 38, 0.98)",
                "button_checked_text": "#7cf5d8",
                "button_checked_border": "#56e8c3",
            },
            "Gold": {
                "background": "#120d08",
                "card": "rgba(24, 18, 12, 0.82)",
                "selector": "rgba(24, 18, 12, 0.72)",
                "border": "rgba(242, 193, 78, 0.18)",
                "border_soft": "rgba(242, 193, 78, 0.14)",
                "title": "#f2c14e",
                "top": "#fff4d5",
                "text": "#fff8e8",
                "muted": "#f5e7bf",
                "accent": "#f2c14e",
                "button": "rgba(35, 27, 18, 0.94)",
                "button_hover": "rgba(49, 39, 26, 0.98)",
                "button_checked_bg": "rgba(67, 48, 19, 0.98)",
                "button_checked_text": "#ffd978",
                "button_checked_border": "#f2c14e",
            },
        }

        self.clock_widget = ClockFaceWidget()
        self.clock_widget.setMaximumSize(560, 560)
        self.clock_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.timer_dialog = TimerDialog()

        self.top_label = QLabel("LISTA CIRCULAR DOBLE")
        self.top_label.setObjectName("topLabel")
        self.top_label.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("RELOJ ANALÓGICO")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.divider = QFrame()
        self.divider.setObjectName("divider")
        self.divider.setFixedHeight(2)
        self.divider.setFixedWidth(360)

        self.current_city_label = QLabel("Bogotá")
        self.current_city_label.setObjectName("currentCityLabel")
        self.current_city_label.setAlignment(Qt.AlignCenter)

        self.date_label = QLabel("--")
        self.date_label.setObjectName("dateLabel")
        self.date_label.setAlignment(Qt.AlignCenter)

        self.previous_button = QPushButton("←")
        self.previous_button.setObjectName("navButton")

        self.next_button = QPushButton("→")
        self.next_button.setObjectName("navButton")

        self.theme_button = QPushButton("Tema: Rosa")
        self.theme_button.setObjectName("secondaryButton")

        self.timer_button = QPushButton("Temporizador")
        self.timer_button.setObjectName("secondaryButton")

        self.city_buttons: dict[str, QPushButton] = {}
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        self._build_ui()
        self._apply_styles()
        self._create_city_buttons()
        self._connect_events()
        self._setup_timers()
        self._apply_current_city()
        self._apply_theme_to_clock()

    def _load_cities(self) -> None:
        cities = [
            ClockCity("Bogotá", -5),
            ClockCity("Nueva York", -4),
            ClockCity("Madrid", 2),
            ClockCity("Tokio", 9),
        ]

        for city in cities:
            self.city_cycle.add_city(city)

    def _build_ui(self) -> None:
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(28, 20, 28, 24)
        root_layout.setSpacing(18)
        root_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        header_layout = QVBoxLayout()
        header_layout.setSpacing(6)
        header_layout.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(self.top_label)
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.divider, alignment=Qt.AlignCenter)

        clock_card = QFrame()
        clock_card.setObjectName("clockCard")
        clock_card.setMaximumWidth(760)

        clock_layout = QVBoxLayout(clock_card)
        clock_layout.setContentsMargins(26, 22, 26, 20)
        clock_layout.setSpacing(8)
        clock_layout.setAlignment(Qt.AlignCenter)

        clock_layout.addWidget(self.clock_widget, alignment=Qt.AlignCenter)
        clock_layout.addWidget(self.current_city_label)
        clock_layout.addWidget(self.date_label)

        selector_card = QFrame()
        selector_card.setObjectName("selectorCard")
        selector_card.setMaximumWidth(980)

        selector_layout = QVBoxLayout(selector_card)
        selector_layout.setContentsMargins(18, 14, 18, 14)
        selector_layout.setSpacing(12)

        navigation_row = QHBoxLayout()
        navigation_row.setSpacing(10)
        navigation_row.setAlignment(Qt.AlignCenter)

        navigation_row.addWidget(self.previous_button)

        self.city_buttons_layout = QHBoxLayout()
        self.city_buttons_layout.setSpacing(10)
        self.city_buttons_layout.setAlignment(Qt.AlignCenter)
        navigation_row.addLayout(self.city_buttons_layout)

        navigation_row.addWidget(self.next_button)

        extras_row = QHBoxLayout()
        extras_row.setSpacing(12)
        extras_row.setAlignment(Qt.AlignCenter)
        extras_row.addWidget(self.theme_button)
        extras_row.addWidget(self.timer_button)

        selector_layout.addLayout(navigation_row)
        selector_layout.addLayout(extras_row)

        root_layout.addLayout(header_layout)
        root_layout.addWidget(clock_card, alignment=Qt.AlignCenter)
        root_layout.addWidget(selector_card, alignment=Qt.AlignCenter)

    def _apply_styles(self) -> None:
        theme_key = self.theme_order[self.current_theme_index]
        palette = self.themes[theme_key]

        self.setStyleSheet(
            f"""
            QWidget#centralWidget {{
                background-color: {palette["background"]};
            }}

            QLabel {{
                background: transparent;
            }}

            QLabel#topLabel {{
                color: {palette["top"]};
                font-size: 18px;
                font-weight: 600;
                padding-top: 6px;
            }}

            QLabel#titleLabel {{
                color: {palette["title"]};
                font-size: 22px;
                font-weight: 800;
                padding-bottom: 2px;
            }}

            QFrame#divider {{
                background-color: {palette["accent"]};
                border-radius: 1px;
            }}

            QFrame#clockCard {{
                background-color: {palette["card"]};
                border: 1px solid {palette["border"]};
                border-radius: 28px;
            }}

            QFrame#selectorCard {{
                background-color: {palette["selector"]};
                border: 1px solid {palette["border_soft"]};
                border-radius: 24px;
            }}

            QLabel#currentCityLabel {{
                color: {palette["text"]};
                font-size: 28px;
                font-weight: 900;
                padding-top: 2px;
            }}

            QLabel#dateLabel {{
                color: {palette["muted"]};
                font-size: 15px;
                font-weight: 700;
                padding-bottom: 4px;
            }}

            QPushButton {{
                background-color: {palette["button"]};
                color: {palette["text"]};
                border: 1px solid {palette["border"]};
                border-radius: 18px;
                padding: 12px 18px;
                font-size: 16px;
                font-weight: 800;
                min-width: 128px;
            }}

            QPushButton:hover {{
                background-color: {palette["button_hover"]};
                border: 1px solid {palette["accent"]};
            }}

            QPushButton:checked {{
                background-color: {palette["button_checked_bg"]};
                color: {palette["button_checked_text"]};
                border: 1px solid {palette["button_checked_border"]};
            }}

            QPushButton#navButton {{
                min-width: 48px;
                max-width: 48px;
                min-height: 48px;
                max-height: 48px;
                border-radius: 24px;
                padding: 0px;
                font-size: 20px;
                font-weight: 900;
            }}

            QPushButton#secondaryButton {{
                min-width: 180px;
            }}
            """
        )

    def _create_city_buttons(self) -> None:
        for city_name in self.city_cycle.city_names():
            button = QPushButton(city_name)
            button.setCheckable(True)
            button.clicked.connect(
                lambda checked=False, name=city_name: self._select_city_by_name(name)
            )

            self.button_group.addButton(button)
            self.city_buttons[city_name] = button
            self.city_buttons_layout.addWidget(button)

    def _connect_events(self) -> None:
        self.previous_button.clicked.connect(self._go_previous_city)
        self.next_button.clicked.connect(self._go_next_city)
        self.theme_button.clicked.connect(self._change_theme)
        self.timer_button.clicked.connect(self._open_timer_dialog)

    def _setup_timers(self) -> None:
        self.live_info_timer = QTimer(self)
        self.live_info_timer.timeout.connect(self._refresh_live_information)
        self.live_info_timer.start(1000)

    def _select_city_by_name(self, city_name: str) -> None:
        self.city_cycle.select_city(city_name)
        self._apply_current_city()

    def _go_previous_city(self) -> None:
        self.city_cycle.previous_city()
        self._apply_current_city()

    def _go_next_city(self) -> None:
        self.city_cycle.next_city()
        self._apply_current_city()

    def _change_theme(self) -> None:
        self.current_theme_index = (self.current_theme_index + 1) % len(self.theme_order)
        theme_key = self.theme_order[self.current_theme_index]
        self.theme_button.setText(f"Tema: {self.theme_labels[theme_key]}")
        self._apply_styles()
        self._apply_theme_to_clock()

    def _apply_theme_to_clock(self) -> None:
        theme_key = self.theme_order[self.current_theme_index]
        self.clock_widget.set_theme(theme_key)

    def _open_timer_dialog(self) -> None:
        self.timer_dialog.show()
        self.timer_dialog.raise_()
        self.timer_dialog.activateWindow()

    def _apply_current_city(self) -> None:
        city = self.city_cycle.current_city()

        if city is None:
            return

        self.current_city_label.setText(city.name)
        self.clock_widget.set_city_time(city.name, city.utc_offset_hours)

        if city.name in self.city_buttons:
            self.city_buttons[city.name].setChecked(True)

        self._refresh_live_information()

    def _refresh_live_information(self) -> None:
        city_time = self._get_current_city_time()
        self.date_label.setText(self._format_spanish_date(city_time))

    def _get_current_city_time(self) -> datetime:
        city = self.city_cycle.current_city()

        if city is None:
            return datetime.now()

        utc_now = datetime.now(timezone.utc)
        return utc_now + timedelta(hours=city.utc_offset_hours)

    def _format_spanish_date(self, moment: datetime) -> str:
        day_names = {
            0: "Lunes",
            1: "Martes",
            2: "Miércoles",
            3: "Jueves",
            4: "Viernes",
            5: "Sábado",
            6: "Domingo",
        }

        month_names = {
            1: "enero",
            2: "febrero",
            3: "marzo",
            4: "abril",
            5: "mayo",
            6: "junio",
            7: "julio",
            8: "agosto",
            9: "septiembre",
            10: "octubre",
            11: "noviembre",
            12: "diciembre",
        }

        return (
            f"{day_names[moment.weekday()]}, "
            f"{moment.day:02d} de {month_names[moment.month]} de {moment.year}"
        )

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Left:
            self._go_previous_city()
            return

        if event.key() == Qt.Key_Right:
            self._go_next_city()
            return

        if event.key() == Qt.Key_B:
            self._select_city_by_name("Bogotá")
            return

        if event.key() == Qt.Key_N:
            self._select_city_by_name("Nueva York")
            return

        if event.key() == Qt.Key_M:
            self._select_city_by_name("Madrid")
            return

        if event.key() == Qt.Key_T:
            self._select_city_by_name("Tokio")
            return

        super().keyPressEvent(event)