from PyQt5.QtWidgets import (
    QWidget, 
    QGroupBox,
    QLabel, 
    QVBoxLayout, 
    QHBoxLayout,
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
        self.bitmap = QPixmap()
        self.pic_label.setPixmap(self.bitmap)
    def _init_widgets(self):
        layout = QHBoxLayout(self)
        self.id = QLabel('id:')
        self.notes = QLabel('notes:')
        vbox_lay = QVBoxLayout()
        SKU_group = QGroupBox('SKU:')
        SKU_group_lay = QVBoxLayout()
        self.SKU_name = QLabel('name:')
        self.SKU_notes = QLabel('notes:')
        SKU_group_lay.addWidget(self.SKU_name)
        SKU_group_lay.addWidget(self.SKU_notes)
        SKU_group.setLayout(SKU_group_lay)
        vbox_lay.addWidget(self.id)
        vbox_lay.addWidget(SKU_group)
        vbox_lay.addWidget(self.notes)
        self.pic_label = QLabel()
        layout.addLayout(vbox_lay)
        layout.addWidget(self.pic_label)
    def setItem(itm):
        pass