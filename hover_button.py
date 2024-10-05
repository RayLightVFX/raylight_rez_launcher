# coding=utf-8

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class HoverButton(QPushButton):
    def __init__(self, parent=None):
        super(HoverButton, self).__init__(parent)
        self.setMouseTracking(True)
        self.normal_size = QSize(50, 50)  # 正常大小
        self.hover_size = QSize(62, 62)  # 悬停时的大小（更大）
        self.setFixedSize(self.hover_size)  # 设置固定大小为最大尺寸
        self.is_hovered = False
        self.original_icon = None

    def setIcon(self, icon):
        self.original_icon = icon
        super().setIcon(icon)

    def enterEvent(self, event):
        self.is_hovered = True
        self.update()
        super(HoverButton, self).enterEvent(event)

    def leaveEvent(self, event):
        self.is_hovered = False
        self.update()
        super(HoverButton, self).leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        if self.original_icon:
            size = self.hover_size if self.is_hovered else self.normal_size
            pixmap = self.original_icon.pixmap(self.original_icon.availableSizes()[-1])  # 使用最大可用尺寸
            scaled_pixmap = pixmap.scaled(size, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)

            x = (self.width() - scaled_pixmap.width()) // 2
            y = (self.height() - scaled_pixmap.height()) // 2

            painter.drawPixmap(x, y, scaled_pixmap)

        # 绘制悬停效果
        if self.is_hovered:
            painter.setBrush(QColor(200, 200, 200, 50))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect(), 8, 8)

        painter.end()