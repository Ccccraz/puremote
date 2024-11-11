from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme


class StyleSheet(StyleSheetBase, Enum):
    """Style sheet"""

    LINK_CARD = "link_card"
    SAMPLE_CARD = "sample_card"
    HOME_INTERFACE = "home_interface"
    ICON_INTERFACE = "icon_interface"
    VIEW_INTERFACE = "view_interface"
    SETTING_INTERFACE = "setting_interface"
    GALLERY_INTERFACE = "gallery_interface"
    NAVIGATION_VIEW_INTERFACE = "navigation_view_interface"

    def path(self, theme=Theme.DARK):
        theme = Theme.DARK
        return f":/qfluentwidgets/qss/{theme.value.lower()}/{self.value}.qss"
