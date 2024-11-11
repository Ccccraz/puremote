from PySide6.QtCore import Property, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

from qfluentwidgets import (
    SimpleCardWidget,
    card_widget,
    setFont,
    FluentStyleSheet,
)


class BaseCard(SimpleCardWidget):
    """Header card widget"""

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.headerView = QWidget(self)
        self.headerLabel = QLabel(self)
        self.separator_header = card_widget.CardSeparator(self)
        self.separator_toolbar = card_widget.CardSeparator(self)
        self.view = QWidget(self)
        self.toolbar_view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self)
        self.headerLayout = QHBoxLayout(self.headerView)
        self.viewLayout = QHBoxLayout(self.view)
        self.toolbar_layout = QHBoxLayout(self.toolbar_view)

        self.headerLayout.addWidget(self.headerLabel)
        self.headerLayout.setContentsMargins(24, 0, 16, 0)
        self.headerView.setFixedHeight(32)
        self.toolbar_layout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetMinimumSize)
        self.toolbar_layout.setContentsMargins(24, 0, 16, 0)
        self.toolbar_view.setFixedHeight(48)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.headerView)
        self.vBoxLayout.addWidget(self.separator_header)
        self.vBoxLayout.addWidget(self.view)
        self.vBoxLayout.addWidget(self.separator_toolbar)
        self.vBoxLayout.addWidget(self.toolbar_view)

        self.viewLayout.setContentsMargins(24, 24, 24, 24)
        setFont(self.headerLabel, 15, QFont.Weight.DemiBold)

        self.view.setObjectName("view")
        self.headerView.setObjectName("headerView")
        self.headerLabel.setObjectName("headerLabel")
        FluentStyleSheet.CARD_WIDGET.apply(self)

        self._postInit()

        self.setTitle(title)

    def getTitle(self):
        return self.headerLabel.text()

    def setTitle(self, title: str):
        self.headerLabel.setText(title)

    def addFunctionButton(self, button):
        self.toolbar_layout.addWidget(button)

    def addFunctionButtons(self, buttons: list):
        for button in buttons:
            self.toolbar_layout.addWidget(button)

        self.toolbar_layout.addStretch(1)

    def removeFunctionButton(self, button):
        self.toolbar_layout.removeWidget(button)

    def _postInit(self):
        pass

    title = Property(str, getTitle, setTitle)
