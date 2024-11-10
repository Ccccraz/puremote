import sys
import vlc
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QFrame,
    QVBoxLayout,
)


class VlcBackend(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)
        self._init_vlc_instance()

    def _init_vlc_instance(self):
        self.instance: vlc.Instance = vlc.Instance()  # type: ignore
        self.media: vlc.Media | None = None
        self.media_player: vlc.MediaPlayer = self.instance.media_player_new()

        self.frame = QFrame()
        self.frame.setMinimumSize(480, 320)
        self.layout_main.addWidget(self.frame)
        self.media_player.set_hwnd(self.frame.winId())

    def set_media(self, media: str) -> None:
        self.media = self.instance.media_new(media)
        self.media_player.set_media(self.media)

    def play(self) -> None:
        self.media_player.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = VlcBackend()
    window.show()

    media = r"./assets/test_anuimal.mp4"
    window.set_media(media)
    window.play()

    sys.exit(app.exec())
