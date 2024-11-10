from PySide6.QtWidgets import QWidget, QGridLayout

from puremote.components.card.base_card import BaseCard
from puremote.components.plotter.plotter_widget import PlotterCard
from puremote.components.trial_monitor.data_monitor_widget import TrialDataCard
from puremote.components.video_monitor.video_monitor_widget import VideoMonitorCard


class ExperimentsInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("experiments_interface")
        self.setStyleSheet(
            "QWidget#experiments_interface {border: none; background:transparent}"
        )

        self._init_ui()

    def _init_ui(self):
        self.layout_main = QGridLayout()
        self.layout_main.setColumnStretch(0, 3)
        self.layout_main.setColumnStretch(1, 7)
        self.layout_main.setRowStretch(0, 7)
        self.layout_main.setRowStretch(1, 3)

        self.plotter_card = PlotterCard(self)
        self.card_video_monitor = VideoMonitorCard()
        self.card_session_data = BaseCard("Session Data")
        self.card_trial_data = TrialDataCard()

        self.layout_main.addWidget(self.plotter_card, 0, 0)
        self.layout_main.addWidget(self.card_video_monitor, 0, 1)
        self.layout_main.addWidget(self.card_session_data, 1, 0)
        self.layout_main.addWidget(self.card_trial_data, 1, 1)

        self.setLayout(self.layout_main)
