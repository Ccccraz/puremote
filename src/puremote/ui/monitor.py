from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton

from puremote.ui.dialog import VideoMontiorDialog
from puremote.ui.gl_backend import GlBackend


class Monitor(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.layout_main = QVBoxLayout()
        self.layout_video = QVBoxLayout()
        self.setLayout(self.layout_main)

        group = QGroupBox("Monitor")
        group.setLayout(self.layout_video)
        self.layout_main.addWidget(group)

        self.button = QPushButton("Link to montior")
        self.button.clicked.connect(self.show_dialog)
        self.layout_video.addWidget(self.button)

    @Slot(str, str)
    def play(self, address: str, backend: str):
        self.layout_video.removeWidget(self.button)
        if backend == "opengl":
            self.player = GlBackend()

        elif backend == "vlc":
            from puremote.ui.vlc_backend import VlcBackend

            self.player = VlcBackend()

        self.player.set_media(address)
        self.layout_video.addWidget(self.player)
        self.player.play()

    def show_dialog(self) -> None:
        dialog = VideoMontiorDialog(self)
        dialog.emit_accepted.connect(self.play)
        dialog.exec()
