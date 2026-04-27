import math
from datetime import datetime, timedelta, timezone

from PySide6.QtCore import QPointF, QRectF, QSize, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPen, QRadialGradient
from PySide6.QtWidgets import QSizePolicy, QWidget


class ClockFaceWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.selected_city = "Bogotá"
        self.utc_offset_hours = -5
        self.theme_name = "Rose"

        self.themes = {
            "Rose": {
                "glow": QColor(205, 106, 255, 30),
                "outer_ring": QColor("#5a415e"),
                "outer_start": QColor("#2b2235"),
                "outer_mid": QColor("#161622"),
                "outer_end": QColor("#0c0d14"),
                "dial_start": QColor("#231727"),
                "dial_mid": QColor("#151321"),
                "dial_end": QColor("#0a0a12"),
                "dial_border": QColor("#2d2331"),
                "major_mark": QColor("#f0eef7"),
                "minor_mark": QColor("#bcaeca"),
                "accent_mark": QColor("#ff8295"),
                "number": QColor("#f6f2ff"),
                "hour_hand": QColor("#ece8f4"),
                "minute_hand": QColor("#ddd7ea"),
                "second_hand": QColor("#ff5a72"),
                "center_outer": QColor("#ff5a72"),
                "center_inner": QColor("#fff4f7"),
            },
            "Emerald": {
                "glow": QColor(72, 212, 180, 28),
                "outer_ring": QColor("#36645d"),
                "outer_start": QColor("#1d312e"),
                "outer_mid": QColor("#101f1d"),
                "outer_end": QColor("#0a1110"),
                "dial_start": QColor("#152725"),
                "dial_mid": QColor("#0f1918"),
                "dial_end": QColor("#091111"),
                "dial_border": QColor("#203735"),
                "major_mark": QColor("#effbf7"),
                "minor_mark": QColor("#a9cfc5"),
                "accent_mark": QColor("#4ce0ba"),
                "number": QColor("#f2fffb"),
                "hour_hand": QColor("#e9faf4"),
                "minute_hand": QColor("#d9f1ea"),
                "second_hand": QColor("#50e3c2"),
                "center_outer": QColor("#50e3c2"),
                "center_inner": QColor("#f4fffb"),
            },
            "Gold": {
                "glow": QColor(242, 193, 78, 26),
                "outer_ring": QColor("#665434"),
                "outer_start": QColor("#352915"),
                "outer_mid": QColor("#211b12"),
                "outer_end": QColor("#120f0b"),
                "dial_start": QColor("#2a2011"),
                "dial_mid": QColor("#1b160f"),
                "dial_end": QColor("#0f0c09"),
                "dial_border": QColor("#3a2d18"),
                "major_mark": QColor("#fff7df"),
                "minor_mark": QColor("#d5c49c"),
                "accent_mark": QColor("#f2c14e"),
                "number": QColor("#fff8e8"),
                "hour_hand": QColor("#fff0cc"),
                "minute_hand": QColor("#f3e3bd"),
                "second_hand": QColor("#f2c14e"),
                "center_outer": QColor("#f2c14e"),
                "center_inner": QColor("#fff9eb"),
            },
        }

        self.setMinimumSize(340, 340)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def sizeHint(self) -> QSize:
        return QSize(540, 540)

    def set_city_time(self, city_name: str, utc_offset_hours: int) -> None:
        self.selected_city = city_name
        self.utc_offset_hours = utc_offset_hours
        self.update()

    def set_theme(self, theme_name: str) -> None:
        if theme_name in self.themes:
            self.theme_name = theme_name
            self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        side = min(width, height)

        center = QPointF(width / 2, height / 2)
        radius = side / 2 - 18

        self._draw_glow(painter, center, radius)
        self._draw_body(painter, center, radius)
        self._draw_marks(painter, center, radius)
        self._draw_numbers(painter, center, radius)
        self._draw_hands(painter, center, radius)
        self._draw_center(painter, center)

    def _palette(self) -> dict:
        return self.themes[self.theme_name]

    def _draw_glow(self, painter: QPainter, center: QPointF, radius: float) -> None:
        palette = self._palette()

        for extra_radius in (18, 12, 6):
            painter.setPen(Qt.NoPen)
            painter.setBrush(palette["glow"])
            painter.drawEllipse(center, radius + extra_radius, radius + extra_radius)

    def _draw_body(self, painter: QPainter, center: QPointF, radius: float) -> None:
        palette = self._palette()

        outer_gradient = QRadialGradient(center, radius)
        outer_gradient.setColorAt(0.0, palette["outer_start"])
        outer_gradient.setColorAt(0.7, palette["outer_mid"])
        outer_gradient.setColorAt(1.0, palette["outer_end"])

        painter.setPen(QPen(palette["outer_ring"], 5))
        painter.setBrush(outer_gradient)
        painter.drawEllipse(center, radius, radius)

        inner_radius = radius - 12
        dial_gradient = QRadialGradient(center, inner_radius)
        dial_gradient.setColorAt(0.0, palette["dial_start"])
        dial_gradient.setColorAt(0.45, palette["dial_mid"])
        dial_gradient.setColorAt(1.0, palette["dial_end"])

        painter.setPen(QPen(palette["dial_border"], 2))
        painter.setBrush(dial_gradient)
        painter.drawEllipse(center, inner_radius, inner_radius)

    def _draw_marks(self, painter: QPainter, center: QPointF, radius: float) -> None:
        palette = self._palette()
        inner_radius = radius - 12

        for index in range(60):
            angle = math.radians(index * 6 - 90)

            if index % 15 == 0:
                outer = self._point(center, inner_radius - 10, angle)
                inner = self._point(center, inner_radius - 34, angle)
                painter.setPen(QPen(palette["accent_mark"], 4, Qt.SolidLine, Qt.FlatCap))
            elif index % 5 == 0:
                outer = self._point(center, inner_radius - 10, angle)
                inner = self._point(center, inner_radius - 30, angle)
                painter.setPen(QPen(palette["major_mark"], 3, Qt.SolidLine, Qt.FlatCap))
            else:
                outer = self._point(center, inner_radius - 12, angle)
                inner = self._point(center, inner_radius - 22, angle)
                painter.setPen(QPen(palette["minor_mark"], 1.5, Qt.SolidLine, Qt.FlatCap))

            painter.drawLine(inner, outer)

    def _draw_numbers(self, painter: QPainter, center: QPointF, radius: float) -> None:
        palette = self._palette()
        inner_radius = radius - 12
        font_size = max(16, int(radius * 0.10))

        font = QFont("Georgia", font_size, QFont.Bold)
        painter.setFont(font)
        painter.setPen(palette["number"])

        for number in range(1, 13):
            angle = math.radians(number * 30 - 90)
            text_point = self._point(center, inner_radius - 66, angle)
            text_rect = QRectF(text_point.x() - 22, text_point.y() - 22, 44, 44)
            painter.drawText(text_rect, Qt.AlignCenter, str(number))

    def _draw_hands(self, painter: QPainter, center: QPointF, radius: float) -> None:
        palette = self._palette()
        current_time = self._get_city_time()

        second_value = current_time.second + current_time.microsecond / 1_000_000
        minute_value = current_time.minute + second_value / 60
        hour_value = (current_time.hour % 12) + minute_value / 60

        hour_angle = math.radians(hour_value * 30 - 90)
        minute_angle = math.radians(minute_value * 6 - 90)
        second_angle = math.radians(second_value * 6 - 90)

        self._draw_hand(
            painter=painter,
            center=center,
            angle=hour_angle,
            length=radius * 0.34,
            width=8,
            color=palette["hour_hand"],
        )

        self._draw_hand(
            painter=painter,
            center=center,
            angle=minute_angle,
            length=radius * 0.56,
            width=5,
            color=palette["minute_hand"],
        )

        self._draw_second_hand(
            painter=painter,
            center=center,
            angle=second_angle,
            forward_length=radius * 0.66,
            backward_length=radius * 0.10,
            width=2,
            color=palette["second_hand"],
        )

    def _draw_hand(
        self,
        painter: QPainter,
        center: QPointF,
        angle: float,
        length: float,
        width: int,
        color: QColor,
    ) -> None:
        end_point = self._point(center, length, angle)
        painter.setPen(QPen(color, width, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(center, end_point)

    def _draw_second_hand(
        self,
        painter: QPainter,
        center: QPointF,
        angle: float,
        forward_length: float,
        backward_length: float,
        width: int,
        color: QColor,
    ) -> None:
        start_point = self._point(center, backward_length, angle + math.pi)
        end_point = self._point(center, forward_length, angle)

        painter.setPen(QPen(color, width, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(start_point, end_point)

    def _draw_center(self, painter: QPainter, center: QPointF) -> None:
        palette = self._palette()

        painter.setPen(Qt.NoPen)
        painter.setBrush(palette["center_outer"])
        painter.drawEllipse(center, 11, 11)

        painter.setBrush(palette["center_inner"])
        painter.drawEllipse(center, 4, 4)

    def _get_city_time(self) -> datetime:
        utc_now = datetime.now(timezone.utc)
        return utc_now + timedelta(hours=self.utc_offset_hours)

    def _point(self, center: QPointF, length: float, angle: float) -> QPointF:
        return QPointF(
            center.x() + math.cos(angle) * length,
            center.y() + math.sin(angle) * length,
        )