import json
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
)
from PySide6.QtGui import QCloseEvent

from puremote.components.trial_monitor.data_monitor_widget import TrialDataMonitor
from puremote.components.session_monitor.session_monitor_widget import (
    SessionDataMonitor,
)
from puremote.components.video_monitor.video_monitor_widget import Monitor
from puremote.components.plotter.plotter_widget import PlotterWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        """Init UI layout"""
        self.setWindowTitle("puremote")

        self.layout_main = QGridLayout()
        self.layout_main.setColumnStretch(0, 3)
        self.layout_main.setColumnStretch(1, 7)
        self.layout_main.setRowStretch(0, 7)
        self.layout_main.setRowStretch(1, 3)
        self.widget_main = QWidget()

        # self._init_menu()
        self._init_plot()
        self._init_monitor()
        self._init_session_monitor()
        self._init_data_monitor()

        self.widget_main.setLayout(self.layout_main)
        self.setCentralWidget(self.widget_main)

    # def _init_menu(self) -> None:
    #     menu = QMenuBar()
    #     open_menu = menu.addMenu("Open")
    #     self.setMenuBar(menu)

    #     action_set_rtsp = QAction(QIcon.fromTheme("document-new"), "rtsp", self)
    #     open_menu.addAction(action_set_rtsp)

    #     action_set_data_listener = QAction("status", self)
    #     open_menu.addAction(action_set_data_listener)

    def _init_plot(self) -> None:
        plotter = PlotterWidget()
        self.layout_main.addWidget(plotter, 0, 0)

    def _init_monitor(self) -> None:
        monitor = Monitor()
        self.layout_main.addWidget(monitor, 0, 1)

    def _init_session_monitor(self) -> None:
        session = SessionDataMonitor()
        self.layout_main.addWidget(session, 1, 0)

    def _init_data_monitor(self) -> None:
        self.data_monitor = TrialDataMonitor()
        self.layout_main.addWidget(self.data_monitor, 1, 1)

    def closeEvent(self, event: QCloseEvent) -> None:
        # self.player.stop()
        return super().closeEvent(event)


if __name__ == "__main__":
    with open(r"../config/default.json", "r") as file:
        config: dict = json.load(file)

    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
