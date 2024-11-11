from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout

from puremote.components.video_monitor.backend.vlc_backend import VlcBackend
from puremote.components.video_monitor.dialog.link_streaming_dialog import (
    LinkStreamingDialog,
)
from puremote.components.card.base_card import BaseCard
from puremote.common.logger import logger
from qfluentwidgets import PrimaryPushButton, FluentIcon

from puremote.components.video_monitor.dialog.record_streaming_dialog import (
    RecordStreamingDialog,
)


class VideoMonitorCard(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._init_ui()
        self.parent_up = parent

    def _init_ui(self):
        self.layout_main = QVBoxLayout()
        self.card = BaseCard(self.tr("Video Monitor"), self)
        self.layout_main.addWidget(self.card)
        self.setLayout(self.layout_main)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setSpacing(0)

        # region create buttons
        self.button_play = PrimaryPushButton(
            FluentIcon.LINK, self.tr("Link to montior"), self
        )
        self.button_record = PrimaryPushButton(FluentIcon.SAVE, self.tr("Record"), self)

        self.button_stop_play = PrimaryPushButton(
            FluentIcon.CLOSE, self.tr("Stop Play"), self
        )
        self.button_stop_record = PrimaryPushButton(
            FluentIcon.CLOSE, self.tr("Stop Record"), self
        )

        self.button_play.clicked.connect(self.show_link_dialog)
        self.button_record.clicked.connect(self.show_record_dialog)
        self.button_stop_play.clicked.connect(self.stop_play)
        self.button_stop_record.clicked.connect(self.stop_record)

        self.card.addFunctionButtons([self.button_play, self.button_record])
        self.card.addFunctionButton(self.button_stop_play)
        self.card.addFunctionButton(self.button_stop_record)
        # endregion

    @Slot(str, bool, str)
    def play(self, address: str, record: bool, target: str):
        print(address, record, target)
        self.video_player = VlcBackend(address, record, target, self)
        self.card.viewLayout.addWidget(self.video_player)

    def record(self, target):
        if self.video_player.recording is not True:
            self.video_player.record(target)

    def stop_play(self):
        try:
            self.video_player.stop_record()
            self.video_player.stop_play()
            self.card.viewLayout.removeWidget(self.video_player)
            self.video_player.deleteLater()
        except AttributeError as e:
            logger.exception(e)

    def stop_record(self):
        try:
            self.video_player.stop_record()
        except AttributeError as e:
            logger.exception(e)

    def show_link_dialog(self) -> None:
        dialog_link = LinkStreamingDialog(self.parent_up)
        dialog_link.emit_accepted.connect(self.play)
        dialog_link.exec()

    def show_record_dialog(self) -> None:
        dialog_record = RecordStreamingDialog(self.parent_up)
        dialog_record.emit_accepted.connect(self.record)
        dialog_record.exec()

    def closeEvent(self, event):
        self.stop_play()
        super().closeEvent(event)
