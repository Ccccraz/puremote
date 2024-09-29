from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QHBoxLayout

from puremote.ui.dialog.dialog_legacy import VideoMontiorDialog
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
        self.video_player = Backend(backend)

        self.video_player.player.set_media(address)
        self.layout_video.insertWidget(self.layout_video.count() - 1, self.video_player)
        self.video_player.player.play()

    def _close(self):
        pass

    def show_dialog(self) -> None:
        dialog = VideoMontiorDialog(self)
        dialog.emit_accepted.connect(self.play)
        dialog.exec()


class Backend(QWidget):
    def __init__(self, backend: str) -> None:
        super().__init__()
        self.backend = backend
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout_video = QVBoxLayout()
        layout_btn = QHBoxLayout()

        layout.addLayout(layout_video)
        layout.addLayout(layout_btn)

        if self.backend == "opengl":
            self.video_player = GlBackend()

        elif self.backend == "vlc":
            from puremote.ui.vlc_backend import VlcBackend

            self.video_player = VlcBackend()

        layout_video.addWidget(self.player)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self._close)
        layout_btn.addWidget(close_btn)

    def _close(self):
        self.close()

    @property
    def player(self):
        return self.video_player
