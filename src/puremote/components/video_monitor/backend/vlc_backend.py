import datetime
from math import fabs
from pathlib import Path
import sys
import vlc
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QFrame,
    QVBoxLayout,
)

from qfluentwidgets import StateToolTip

from puremote.common.logger import logger


class VlcBackend(QWidget):
    def __init__(
        self,
        address,
        record: bool = False,
        target_floder: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.need_record = record
        self.target_floder = target_floder
        self.playing = False
        self.recording = False

        self.layout_main = QVBoxLayout(self)
        self.setLayout(self.layout_main)
        self.address = address
        self._init_vlc_instance()

    def _init_vlc_instance(self):
        self.instance: vlc.Instance = vlc.Instance()  # type: ignore
        self.media: vlc.Media = self.instance.media_new(self.address)
        self.media_player: vlc.MediaPlayer = self.instance.media_player_new()
        self.media_player.set_media(self.media)

        self.frame = QFrame(self)
        self.frame.setMinimumSize(480, 320)
        self.layout_main.addWidget(self.frame)
        self.media_player.set_hwnd(self.frame.winId())

        self.play()
        self.playing = True

    def play(self) -> None:
        self.media_player.play()

        if self.need_record:
            self.record(self.target_floder)

    def record(self, target_floder: str) -> None:
        target_file_new = (
            Path(target_floder)
            / f"{datetime.datetime.now().strftime(r"%Y%m%d_%H%M%S")}.mp4"
        )
        self.media_record: vlc.Media = self.instance.media_new(self.address)
        self.media_record.add_option(f"sout=#file{{dst={target_file_new}}}")
        self.media_record.add_option("sout-keep")
        self.media_recorder: vlc.MediaPlayer = self.instance.media_player_new()
        self.media_recorder.set_media(self.media_record)
        self.media_recorder.play()
        self.recording = True
        logger.info(f"record to {target_file_new}")

        self.stateTooltip = StateToolTip(
            self.tr("Recording"), str(target_file_new), self.window()
        )
        self.stateTooltip.move(self.stateTooltip.getSuitablePos())
        self.stateTooltip.show()

    def stop_play(self) -> None:
        if self.playing:
            self.media.release()
            self.media_player.stop()
            self.playing = False
        else:
            logger.warning("not playing")

    def stop_record(self) -> None:
        if self.recording:
            self.media_record.release()
            self.media_recorder.stop()
            self.recording = False
            logger.info("stop record")
            assert self.stateTooltip is not None
            self.stateTooltip.setContent(self.tr("Stop Recording"))
            self.stateTooltip.setState(True)
            self.stateTooltip = None
        else:
            logger.warning("not recording")


if __name__ == "__main__":
    pass
    # app = QApplication(sys.argv)

    # window = VlcBackend("", None)
    # window.show()

    # media = r"./assets/test_anuimal.mp4"
    # window.set_media(media)
    # window.play()

    # sys.exit(app.exec())
