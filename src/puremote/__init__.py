from puremote.env_variable import CONFIG  # noqa: F401

import sys
from PySide6 import QtWidgets

from puremote.ui.main_view import MainWindow


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
