import json
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMenuBar,
    QGroupBox,
    QPushButton,
)
from PySide6.QtGui import QAction, QCloseEvent, QIcon
from PySide6.QtCore import Slot, Qt

from puremote.ui.dialog import RtspDialog, StatusDialog
from puremote.ui.data_table_view import DataTableView
from puremote.ui.gl_backend import GlBackend
from puremote.ui.vlc_backend import VlcBackend


class MainWindow(QMainWindow):
    def __init__(self, config: dict) -> None:
        super().__init__()
        self._config: dict = config
        self._init_ui()

    def _init_ui(self) -> None:
        """Init UI layout"""
        self.setWindowTitle("psychounity remote controller")

        self.widget_main = QWidget()
        self.layout_main = QVBoxLayout()
        self.layout_plot_monitor = QHBoxLayout()
        self.layout_main.addLayout(self.layout_plot_monitor)

        self._init_menu()
        self._init_plot()
        self._init_player()
        self._init_table_view()

        self.widget_main.setLayout(self.layout_main)
        self.setCentralWidget(self.widget_main)

    def _init_menu(self) -> None:
        menu = QMenuBar()
        open_menu = menu.addMenu("Open")
        self.setMenuBar(menu)

        action_set_rtsp = QAction(QIcon.fromTheme("document-new"), "rtsp", self)
        action_set_rtsp.triggered.connect(self._init_rtsp_dialog)
        open_menu.addAction(action_set_rtsp)

        action_set_data_listener = QAction("status", self)
        action_set_data_listener.triggered.connect(self._init_status_dialog)
        open_menu.addAction(action_set_data_listener)

    def _init_rtsp_dialog(self) -> None:
        dialog = RtspDialog(self, self._config)
        dialog.emit_accepted.connect(self._play_video)
        dialog.exec()

    def _init_status_dialog(self) -> None:
        dialog = StatusDialog(self, self._config)
        dialog.emit_accept.connect(self._listening)
        dialog.exec()

    def _init_table_view(self) -> None:
        self.data_table = DataTableView()

        layout = QVBoxLayout()
        layout.addWidget(self.data_table)
        group = QGroupBox("Data")
        group.setMaximumHeight(240)
        group.setLayout(layout)

        self.layout_main.addWidget(group)

    @Slot(str)
    def _listening(self, address: str) -> None:
        self.data_table.init_listener(address)

    # Init player ui
    def _init_player(self) -> None:
        self.button_rtsp = QPushButton("Connect to CCTV")
        self.button_rtsp.clicked.connect(self._init_rtsp_dialog)

        self.player_layout = QVBoxLayout()
        self.player_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.player_layout.addWidget(self.button_rtsp)

        groupbox = QGroupBox("Monitor")
        groupbox.setLayout(self.player_layout)
        groupbox.setMinimumSize(640, 320)

        self.layout_plot_monitor.addWidget(groupbox)

    # Init player and play video
    @Slot(str, str)
    def _play_video(self, address: str, backend: str) -> None:
        self.player_layout.removeWidget(self.button_rtsp)

        if backend == "vlc":
            self.player = VlcBackend()

        elif backend == "opengl":
            self.player = GlBackend()

        self.player.set_media(address)
        self.player_layout.addWidget(self.player)
        self.player.play()

    def _init_plot(self) -> None:
        groupbox = QGroupBox("Plot")
        self.layout_plot = QVBoxLayout()
        groupbox.setLayout(self.layout_plot)
        groupbox.setMaximumWidth(320)
        self.pushbutton_add_plot = QPushButton("Add a figure")
        self.layout_plot.addWidget(self.pushbutton_add_plot)
        self.layout_plot_monitor.addWidget(groupbox)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.data_table.stop()
        # self.player.stop()
        return super().closeEvent(event)


if __name__ == "__main__":
    with open(r"../config/default.json", "r") as file:
        config: dict = json.load(file)

    app = QApplication(sys.argv)

    main_window = MainWindow(config)
    main_window.show()

    sys.exit(app.exec())
