from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, SplashScreen, setTheme, Theme, FluentIcon
from puremote.config.config import APP_NAME
from puremote.views.experiments_view.experiments_view import ExperimentsInterface


class MainWindow(FluentWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initWindow()

        setTheme(Theme.DARK)

        self.experiments_interface = ExperimentsInterface(self)

        self.initNavigation()

        self.splashScreen.finish()

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        # self.setWindowIcon(QIcon(":/gallery/images/logo.png"))
        self.setWindowTitle(APP_NAME)

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def initNavigation(self):
        self.addSubInterface(self.experiments_interface, FluentIcon.CAMERA, "Monitor")
