import sys
import json

from PySide6 import QtWidgets

from puremote.ui.main_view import MainWindow


def main() -> None:
    with open(r"config/default.json", "r") as file:
        config = json.load(file)

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow(config)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
