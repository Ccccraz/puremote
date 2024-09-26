from PySide6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QPushButton


class SessionDataMonitor(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.layout_main = QVBoxLayout()
        self.layout_session = QVBoxLayout()

        group = QGroupBox("Session data")
        group.setLayout(self.layout_session)
        self.layout_main.addWidget(group)

        button = QPushButton("link")
        self.layout_session.addWidget(button)

        self.setLayout(self.layout_main)
