from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout

from puremote.components.video_monitor.dialog.link_streaming_dialog import (
    LinkStreamingDialog,
)
from puremote.components.video_monitor.backend.gl_backend import GlBackend
from puremote.components.card.base_card import BaseCard
from qfluentwidgets import PrimaryPushButton, FluentIcon


class VideoMonitorCard(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.layout_main = QVBoxLayout()
        self.card = BaseCard(self.tr("Video Monitor"))
        self.layout_main.addWidget(self.card)
        self.setLayout(self.layout_main)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setSpacing(0)

        self.button = PrimaryPushButton(
            FluentIcon.LINK, self.tr("Link to montior"), self
        )
        self.button.clicked.connect(self.show_dialog)

        self.card.addFunctionButton([self.button])

    @Slot(str, str)
    def play(self, address: str, backend: str):
        if backend == "opengl":
            self.video_player = GlBackend()

        elif backend == "vlc":
            from puremote.components.video_monitor.backend.vlc_backend import VlcBackend

            self.video_player = VlcBackend()

        self.video_player.set_media(address)
        self.card.viewLayout.addWidget(self.video_player)
        self.video_player.play()

    def _close(self):
        pass

    def show_dialog(self) -> None:
        dialog = LinkStreamingDialog(self)
        dialog.emit_accepted.connect(self.play)
        dialog.exec()
