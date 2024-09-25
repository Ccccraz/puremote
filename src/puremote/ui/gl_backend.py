import sys

from loguru import logger

from threading import Thread

from PySide6.QtCore import QSize, QPoint
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtGui import QCloseEvent, QImage, QResizeEvent
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtOpenGL import QOpenGLTexture

from OpenGL import GL as gl

from vidgear.gears import CamGear


class GLVideoViewerBase(QOpenGLWidget):
    def __init__(self) -> None:
        super().__init__()
        self.frame: QImage | None = None

    def initializeGL(self) -> None:
        gl.glClearColor(0, 0, 0, 1)
        gl.glEnable(gl.GL_TEXTURE_2D)

    def resizeGL(self, w: int, h: int) -> None:
        gl.glViewport(0, 0, w, h)

    def paintGL(self) -> None:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)  # type: ignore

        self.texture = QOpenGLTexture(QOpenGLTexture.Target.Target2D)
        self.texture.create()
        self.texture.setMinificationFilter(QOpenGLTexture.Filter.LinearMipMapLinear)
        self.texture.setMagnificationFilter(QOpenGLTexture.Filter.Linear)

        if self.frame is not None:
            self.texture.setData(self.frame)
            self.texture.setWrapMode(QOpenGLTexture.WrapMode.ClampToEdge)

            self.texture.bind()

            gl.glBegin(gl.GL_QUADS)
            gl.glTexCoord2f(0.0, 1.0)
            gl.glVertex3f(-1.0, -1.0, 0.0)  # Bottom-left corner
            gl.glTexCoord2f(1.0, 1.0)
            gl.glVertex3f(1.0, -1.0, 0.0)  # Bottom-right corner
            gl.glTexCoord2f(1.0, 0.0)
            gl.glVertex3f(1.0, 1.0, 0.0)  # Top-right corner
            gl.glTexCoord2f(0.0, 0.0)
            gl.glVertex3f(-1.0, 1.0, 0.0)  # Top-left corner
            gl.glEnd()

        self.texture.release()
        self.texture.destroy()

    def update_frame(self, frame: QImage) -> None:
        self.frame = frame
        self.update()


class GlBackend(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._init_ui()
        self.source: str | None = None
        self.aspect_ratio: float | None = None
        self.playing = False

    def resizeEvent(self, event: QResizeEvent) -> None:
        if self.aspect_ratio is not None:
            size = event.size()
            w = size.width()
            h = size.height()

            scale_w = int(h * self.aspect_ratio)
            scale_h = int(w / self.aspect_ratio)

            if scale_w < w:
                new_size = QSize(scale_w, h)
                new_point = QPoint(int(w - scale_w / 2), 0)
            else:
                new_size = QSize(w, scale_h)
                new_point = QPoint(0, int(h - scale_h / 2))

            self.viewer.resize(new_size)
            self.viewer.setProperty("pos", new_point)

        super().resizeEvent(event)

    def _init_ui(self) -> None:
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        self.viewer = GLVideoViewerBase()
        self.layout_main.addWidget(self.viewer)

    def set_media(self, source: str, fps: int | None = None) -> None:
        self.source = source
        self.fps: int | None = fps

    def play(self) -> None:
        if self.source is None:
            logger.warning("Video source doesn't setup")

        self.stream = CamGear(source=self.source, colorspace="COLOR_BGR2RGB").start()  # type: ignore

        need_init = True
        while need_init:
            frame = self.stream.read()

            if frame is None:
                break

            height, width, channels = frame.shape
            self.aspect_ratio = width / height
            QApplication.sendEvent(self, QResizeEvent(self.size(), self.size()))
            need_init = False

        self.play_thread = Thread(target=self._playing)

        self.playing = True

        self.play_thread.start()

    def _playing(self) -> None:
        while self.playing:
            frame = self.stream.read()

            if frame is None:
                break

            height, width, channels = frame.shape
            self.aspect_ratio = width / height

            q_frame = QImage(
                frame.data,
                width,
                height,
                width * channels,
                QImage.Format.Format_RGB888,
            )

            self.viewer.update_frame(q_frame)

    def stop(self) -> None:
        if self.playing:
            logger.info("stopping glviewer widget...")
            self.playing = False
            self.play_thread.join()
            logger.info("glviewer widget stopped")


if __name__ == "__main__":

    class MainWindow(QMainWindow):
        def __init__(self) -> None:
            super().__init__()
            self._init_ui()
            self.viewer.set_media(r"assets\test_anuimal.mp4")
            self.viewer.play()

        def closeEvent(self, event: QCloseEvent) -> None:
            self.viewer.stop()
            return super().closeEvent(event)

        def _init_ui(self) -> None:
            self.widget = QWidget()
            self.layout_main = QVBoxLayout()
            self.setCentralWidget(self.widget)
            self.widget.setLayout(self.layout_main)

            self.viewer = GlBackend()
            self.layout_main.addWidget(self.viewer)

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
