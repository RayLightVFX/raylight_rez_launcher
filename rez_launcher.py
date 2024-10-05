# coding=utf-8

import os
import json
import logging
import threading

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from hover_button import HoverButton
import rez_resolved_context

logger = logging.getLogger(__name__)

PROJECT_PATH = r'\\10.6.9.26\rez\project'


def qss_style():
    qss_path = os.path.join(os.path.dirname(__file__), 'resources', "raylight.qss")
    if os.path.isfile(qss_path):
        with open(qss_path, "r", encoding='utf-8') as f:
            return f.read()
    else:
        return ""


class RezLauncher(QWidget):
    BUTTON_SIZE = 50
    BORDER_RADIUS = 8  # 控制圆角大小的常量
    button_clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super(RezLauncher, self).__init__(parent)
        self.setObjectName("RezLauncher")
        self.project_combobox = None
        self.initUI()
        self.setFixedHeight(100)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # 隐藏标题栏
        self.oldPos = self.pos()

        self.add_project_package()
        self.moveToTaskbar()

    def initUI(self):
        self.setWindowIcon(QIcon('resources\logo.ico'))
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setLayout(layout)

        # 添加项目
        project_layout = QHBoxLayout()
        project_widget = QWidget()
        project_widget.setObjectName("ProjectWidget")
        project_widget.setLayout(project_layout)
        project_layout.setContentsMargins(10, 5, 10, 5)
        project_layout.addWidget(QLabel("Project:"))
        project_combobox = QComboBox()
        project_combobox.setFixedSize(QSize(80, 22))
        self.project_combobox = project_combobox
        project_layout.addWidget(project_combobox)
        project_layout.addStretch()
        project_widget.setFixedSize(QSize(600, 30))
        layout.addWidget(project_widget)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 5, 10, 5)
        button_layout.setSpacing(5)  # 减小间距
        layout.addLayout(button_layout)

        # 定义要创建的 DCC 按钮列表
        dcc_list = [
            "maya", "houdini", "rv", "nuke", "nukex", "hiero", "katana",
            "deadlinemonitor", "showdashboard", "mandaytool",
        ]

        # 循环创建按钮并添加到布局中
        for dcc_name in dcc_list:
            button = self._get_dcc_button(dcc_name)
            button_layout.addWidget(button)

    def _get_dcc_button(self, dcc_name):
        button = HoverButton(self)

        # 设置工具提示
        button.setToolTip(dcc_name)

        # 设置圆角图标
        icon_path = self._find_icon(dcc_name)
        if icon_path:
            round_icon = self._create_round_icon(icon_path)
            button.setIcon(round_icon)

        # 连接点击信号
        button.clicked.connect(lambda: self._on_button_clicked(dcc_name))

        return button

    def _create_round_icon(self, icon_path):
        original_pixmap = QPixmap(icon_path)
        target_size = max(self.BUTTON_SIZE, 100)  # 使用更大的初始尺寸

        # 创建一个圆角的 pixmap
        rounded_pixmap = QPixmap(target_size, target_size)
        rounded_pixmap.fill(QColor(0, 0, 0, 0))

        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # 创建一个圆角路径
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, target_size, target_size), self.BORDER_RADIUS, self.BORDER_RADIUS)

        # 将原始图标缩放到目标大小，保持宽高比
        scaled_pixmap = original_pixmap.scaled(
            target_size, target_size, Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)

        # 计算居中位置
        x_offset = (target_size - scaled_pixmap.width()) / 2
        y_offset = (target_size - scaled_pixmap.height()) / 2

        # 使用路径作为裁剪区域
        painter.setClipPath(path)

        # 绘制缩放后的图标
        painter.drawPixmap(int(x_offset), int(y_offset), scaled_pixmap)

        painter.end()

        return QIcon(rounded_pixmap)

    def _find_icon(self, dcc_name):
        extensions = ['.png', '.jpg', '.svg', '.ico']

        # 图标文件夹路径
        icon_folder = os.path.join(os.path.dirname(__file__), 'resources', 'icon')

        # 尝试不同的文件名格式和扩展名
        possible_names = [
            dcc_name.lower(),
            dcc_name.upper(),
            dcc_name.capitalize(),
            f"{dcc_name.lower()}",
        ]

        for name in possible_names:
            for ext in extensions:
                icon_path = os.path.join(icon_folder, name + ext)
                if os.path.isfile(icon_path):
                    return icon_path

        print(f"Warning: Icon not found for {dcc_name}")
        return None

    def add_project_package(self):
        try:
            server_project = os.listdir(PROJECT_PATH)
            for project in server_project:
                self.project_combobox.addItem(project)
        except Exception as e:
            print(e)

    def _on_button_clicked(self, dcc_name):
        self.button_clicked.emit(dcc_name)
        env_name = self.project_combobox.currentText()

        # 创建并启动线程
        thread = threading.Thread(target=self._launch_dcc, args=(dcc_name, env_name))
        thread.start()

    def _launch_dcc(self, dcc_name, env_name):
        rez_resolved_context.launcher([env_name], dcc_name)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

    def moveToTaskbar(self):
        screen = QGuiApplication.primaryScreen()
        screenRect = screen.availableGeometry()
        window_height = self.frameGeometry().height()
        new_y_position = screenRect.height() - window_height
        self.move((screenRect.width() - self.frameGeometry().width()) // 2, new_y_position)


if __name__ == '__main__':
    app = QApplication([])
    app.setStyleSheet(qss_style())
    app.setWindowIcon(QIcon('resource/logo.ico'))
    widget = RezLauncher()
    widget.show()
    app.exec()
