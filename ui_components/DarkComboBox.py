from PySide6.QtWidgets import QComboBox

import colors


class DarkComboBox(QComboBox):
    """
    This class extends QComboBox to create a combo box that adapts to light/dark themes.
    Args:
        items (list): A list of items to be added to the combo box.
    """
    def __init__(self, items):
        super().__init__()

        self.addItems(items)
        
        view = self.view()
        view.setMouseTracking(True)  
        view.setAutoScroll(False) 
        view.setStyleSheet(F"""
            QAbstractItemView {{
                show-decoration-selected: 1; 
                outline: 0;
            }}
            QAbstractItemView::item {{
                padding: 2px;
                border-left: 1px solid transparent; 
            }}
            QAbstractItemView::item:selected {{
                background-color: {colors.COMBO_ITEM_HOVER};  
                border-left: 1px solid {colors.COMBO_SELECTED}; 
            }}
        """)

        self.setStyleSheet(F"""
            QComboBox {{
                padding: 5px;
                padding: 5px; 
                padding-left: 10px; 
                background-color: {colors.COMBO_BACKGROUND};
            }}
        """)

         
      