from PyQt5.QtWidgets import (
    QWidget, 
    QListView,
    QLineEdit,
    QVBoxLayout, 
    QGridLayout, 
    QPushButton,
    QLabel
)
from .item_viewer import InventoryItemViewer

class InventoryFrm(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.init_widgets()
    def init_widgets(self):
        layout = QVBoxLayout(self)
        inventory_view = InventoryView()
        item_viewer = InventoryItemViewer()
        layout.addWidget(inventory_view)
        layout.addWidget(item_viewer)


class InventoryView(QWidget):
    """Provides a read-only view of the inventory database
    plus buttons to open editing dialogs. 

    This class abstracts away the actual view widgets and 
    their directly related editing controls from the inventory form. 
    """
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.init_widgets()
    def init_widgets(self):
        #buttons related to viewer widget
        self.layout = QGridLayout()
        self.layout.addWidget(QLabel("Categories"), 0, 0)
        self.layout.addWidget(QLabel("SKUs"), 0, 1)
        self.layout.addWidget(QLabel("Items"), 0, 2)
        self.filter_by_cat = QPushButton("Filter by Category")
        self.clear_cat_selection = QPushButton("Clear Selection")
        self.search_SKUs_input = QLineEdit()
        self.search_SKUs_btn = QPushButton("Search in SKUs")
        self.show_item_hist = QPushButton("Show Item History")
        self.layout.addWidget(self.filter_by_cat, 1, 0)
        self.layout.addWidget(self.clear_cat_selection, 2, 0)
        self.layout.addWidget(self.search_SKUs_input, 1, 1)
        self.layout.addWidget(self.search_SKUs_btn, 2, 1)
        self.layout.addWidget(self.show_item_hist, 2, 2)
        self.categories = QListView()
        self.SKUs = QListView()
        self.inv_items = QListView()
        self.layout.addWidget(self.categories, 3, 0)
        self.layout.addWidget(self.SKUs, 3, 1)
        self.layout.addWidget(self.inv_items, 3, 2)
        self.new_category = QPushButton("New Category")
        self.del_category = QPushButton("Del Category")
        self.edit_category = QPushButton("Edit Category")
        self.new_SKU = QPushButton("New SKU")
        self.edit_SKU = QPushButton("Edit SKU")
        self.add_item_to_SKU = QPushButton("Add Item to SKU")
        self.edit_item = QPushButton("Edit Item")
        self.layout.addWidget(self.new_category, 4, 0)
        self.layout.addWidget(self.edit_category, 5, 0)
        self.layout.addWidget(self.del_category, 6, 0)
        self.layout.addWidget(self.new_SKU, 4, 1)
        self.layout.addWidget(self.edit_SKU, 5, 1)
        self.layout.addWidget(self.add_item_to_SKU, 4, 2)
        self.layout.addWidget(self.edit_item, 5, 2)
        self.itm_deletion_hint = QLabel("No 'delete' for history consistency. Move to other category instead.")
        self.itm_deletion_hint.setWordWrap(1)
        self.layout.addWidget(self.itm_deletion_hint, 6, 1, 1, 2)
        self.setLayout(self.layout)
    def set_model(table_model, category_col_id, SKU_col_id):
        """Connect the view to a flat table model.

        :param table_model: Flat db-type table model
        :type table_model: QAbstractTableModel
        :param category_col_id: id of the column containing categories
        :type category_col_id: int
        :param SKU_col_id: id of the column with SKUs
        :type SKU_col_id: int
        """