from PyQt5.QtWidgets import QWidget, QColumnView, QVBoxLayout, QGridLayout, QPushButton

class InventoryFrm(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.init_widgets()
    def init_widgets(self):
        layout = QVBoxLayout(self)
        inventory_viewer = InventoryViewer()
        layout.addWidget(inventory_viewer)

class InventoryViewer(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.init_widgets()
    def init_widgets(self):
        #buttons related to viewer widget
        btn_layout = QGridLayout()
        new_category = QPushButton("New Category")
        del_category = QPushButton("Del Category")
        new_SKU = QPushButton("New SKU")
        add_item_to_SKU = QPushButton("Add Item to SKU")
        btn_layout.addWidget(new_category, 0, 0)
        btn_layout.addWidget(del_category, 1, 0)
        btn_layout.addWidget(new_SKU, 0, 1)
        btn_layout.addWidget(add_item_to_SKU, 0, 2)

        layout = QVBoxLayout()
        table = QColumnView()
        layout.addWidget(table)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

class ItemFrm(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)