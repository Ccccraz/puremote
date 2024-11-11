from pathlib import Path
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QFrame,
    QVBoxLayout,
)
from PySide6.QtMultimedia import QMediaPlayer, QMediaRecorder
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl


class NativeBackend(QWidget):
    def __init__(self, address, parent) -> None:
        super().__init__(parent=parent)
        self.address = QUrl(address)
        self.main_layout = QVBoxLayout()
        self.play()

    def play(self):
        player = QMediaPlayer(self)
        player.setSource(QUrl("rtsp://localhost/live"))
        video_widget = QVideoWidget(self)
        self.main_layout.addWidget(video_widget)
        player.setVideoOutput(video_widget)
        player.play()

    def record(self):
        pass

    def stop(self):
        pass


if __name__ == "__main__":
    import os

    os.environ["QT_MEDIA_BACKEND"] = "ffmpeg"
    app = QApplication(sys.argv)
    widget = NativeBackend("rtsp://localhost/live", None)
    widget.show()
    sys.exit(app.exec())
