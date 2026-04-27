import math
from datetime import datetime

from PySide6.QtCore import QPointF, QRectF, QSize, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget


class ClockFaceWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setMinimumSize(520, 520)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def sizeHint(self) -> QSize:
        return QSize(700, 700)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        side = min(width, height)

        center = QPointF(width / 2, height / 2)
        radius = side / 2 - 40

        self._draw_shadow(painter, center, radius)
        self._draw_body(painter, center, radius)
        self._draw_marks(painter, center, radius)
        self._draw_numbers(painter, center, radius)
        self._draw_hands(painter, center, radius)
        self._draw_center(painter, center)

    def _draw_shadow(self, painter: QPainter, center: QPointF, radius: float) -> None:
        for extra_radius, alpha in [(18, 18), (12, 28), (6, 38)]:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 0, 0, alpha))
            painter.drawEllipse(center, radius + extra_radius, radius + extra_radius)

    def _draw_body(self, painter: QPainter, center: QPointF, radius: float) -> None:
        painter.setPen(QPen(QColor("#1f1f22"), 20))
        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(center, radius, radius)

        painter.setPen(QPen(QColor("#2d2d31"), 4))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(center, radius - 12, radius - 12)

    def _draw_marks(self, painter: QPainter, center: QPointF, radius: float) -> None:
        for index in range(60):
            angle = math.radians(index * 6 - 90)

            if index % 5 == 0:
                outer = self._point(center, radius - 20, angle)
                inner = self._point(center, radius - 58, angle)
                painter.setPen(QPen(QColor("#000000"), 10, Qt.SolidLine, Qt.FlatCap))
            else:
                outer = self._point(center, radius - 20, angle)
                inner = self._point(center, radius - 42, angle)
                painter.setPen(QPen(QColor("#000000"), 4, Qt.SolidLine, Qt.FlatCap))

            painter.drawLine(inner, outer)

    def _draw_numbers(self, painter: QPainter, center: QPointF, radius: float) -> None:
        font_size = max(20, int(radius * 0.16))
        painter.setFont(QFont("Arial", font_size, QFont.Bold))
        painter.setPen(QColor("#000000"))

        for number in range(1, 13):
            angle = math.radians(number * 30 - 90)
            text_point = self._point(center, radius - 100, angle)
            text_rect = QRectF(text_point.x() - 32, text_point.y() - 32, 64, 64)
            painter.drawText(text_rect, Qt.AlignCenter, str(number))

    def _draw_hands(self, painter: QPainter, center: QPointF, radius: float) -> None:
        now = datetime.now()

        second_value = now.second + now.microsecond / 1_000_000
        minute_value = now.minute + second_value / 60
        hour_value = (now.hour % 12) + minute_value / 60

        hour_angle = math.radians(hour_value * 30 - 90)
        minute_angle = math.radians(minute_value * 6 - 90)
        second_angle = math.radians(second_value * 6 - 90)

        self._draw_hand(
            painter=painter,
            center=center,
            angle=hour_angle,
            forward_length=radius * 0.48,
            backward_length=radius * 0.12,
            width=12,
            color=QColor("#000000"),
        )

        self._draw_hand(
            painter=painter,
            center=center,
            angle=minute_angle,
            forward_length=radius * 0.72,
            backward_length=radius * 0.10,
            width=8,
            color=QColor("#000000"),
        )

        self._draw_hand(
            painter=painter,
            center=center,
            angle=second_angle,
            forward_length=radius * 0.78,
            backward_length=radius * 0.16,
            width=2,
            color=QColor("#000000"),
        )

    def _draw_hand(
        self,
        painter: QPainter,
        center: QPointF,
        angle: float,
        forward_length: float,
        backward_length: float,
        width: int,
        color: QColor,
    ) -> None:
        painter.setPen(QPen(color, width, Qt.SolidLine, Qt.RoundCap))

        start_point = self._point(center, backward_length, angle + math.pi)
        end_point = self._point(center, forward_length, angle)

        painter.drawLine(start_point, end_point)

    def _draw_center(self, painter: QPainter, center: QPointF) -> None:
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#111111"))
        painter.drawEllipse(center, 11, 11)

        painter.setBrush(QColor("#3d3d3d"))
        painter.drawEllipse(center, 5, 5)

    def _point(self, center: QPointF, length: float, angle: float) -> QPointF:
        return QPointF(
            center.x() + math.cos(angle) * length,
            center.y() + math.sin(angle) * length,
        )