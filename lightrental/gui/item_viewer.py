from PyQt5.QtWidgets import (
    QWidget, 
    QGroupBox,
    QLabel, 
    QVBoxLayout, 
    QHBoxLayout
)
from PyQt5.QtGui import QPixmap

class InventoryItemViewer(QWidget):
    """Read-only preview panel for a rental item.

    Works both with inventory and history items since it doesn't
    know their peculiarities and just displays an InventoryItem object.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._init_widgets()
    def _init_widgets(self):
        layout = QHBoxLayout(self)
        id = QLabel('id:')
        notes = QLabel('notes:')
        vbox_lay = QVBoxLayout()
        SKU_group = QGroupBox('SKU:')
        SKU_group_lay = QVBoxLayout()
        SKU_name = QLabel('name:')
        SKU_notes = QLabel('notes:')
        SKU_group_lay.addWidget(SKU_name)
        SKU_group_lay.addWidget(SKU_notes)
        SKU_group.setLayout(SKU_group_lay)
        vbox_lay.addWidget(id)
        vbox_lay.addWidget(SKU_group)
        vbox_lay.addWidget(notes)
        pic_label = QLabel()
        layout.addLayout(vbox_lay)
        layout.addWidget(pic_label)
    def setItem(itm):
        pass