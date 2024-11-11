import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from puremote.views.main_view import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
