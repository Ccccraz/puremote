from PySide6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QPushButton


class PlotterWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.layout_main = QVBoxLayout()
        self.layout_session = QVBoxLayout()

        group = QGroupBox("figure")
        group.setLayout(self.layout_session)
        self.layout_main.addWidget(group)

        button = QPushButton("add figure")
        self.layout_session.addWidget(button)

        self.setLayout(self.layout_main)
