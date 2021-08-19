"""
Model types for the Model-View GUI.

Adapts the functionality of 'database' module to Qt's MV
interfaces so that it can be easily acessed from GUI
without directly calling database.py functions and
worrying about integrity.
"""

from PyQt5.QtWidgets import (
    QRelationalTableModel
)
from collections import namedtuple
# uses InventoryDB interface

InventoryItem = namedtuple(
    "InventoryItem", 
    ['nr', 'SKU', 'category', 'notes', 'imgpath'],
    defaults=['', '']    # notes='' - applied right to left
)
InventorySKU = namedtuple(
    "InventorySKU",
    ['SKU', 'name', 'notes'],
    defaults=['']    # notes='' - applied right to left
)
InventoryCategory = namedtuple(
    "InventoryCategory",
    ['id', 'name', 'notes'],
    defaults=['']    # notes='' - applied right to left
)

class InventoryModel(QRelationalTableModel):
    def __init__(self, db) -> None:
        """Construct a Qt model that uses a given InventoryDB

        :param db: database SQL wrapper object
        :type db: InventoryDB
        """
        super().__init__(db.connection_handle())
        self.db = db
        super().setTable(self.db.inventory_table_name())
        col, rel = self.db.SKU_relation()
        super().setRelation(col, rel)
        col, rel = self.db.category_relation()
        super().setRelation(col, rel)
    def add_item(self, item):
        self.db.add_item(
            nr=item.nr,
            SKU=item.SKU,
            category=item.category
        )
    def add_SKU(self, sku_obj, item):
        """Add an SKU to the DB. 

        Since SKUs cannot be empty, at least one item
        belonging to it must be provided.

        :param sku_obj: SKU to be added
        :type sku_obj: InventorySKU namedtuple
        :param item: first item to be added to the SKU - they cannot be empty
        :type item: InventoryItem namedtuple
        :return: None
        :rtype: [type]
        """
        if not sku_obj.SKU == item.SKU:
            return None
            # TODO: raise error
        self.db.add_SKU(
            SKU = sku_obj.SKU,
            sku_name = sku_obj.name,
            sku_notes = sku_obj.notes,
            itm_nr=item.nr,
            itm_cat=item.category,
            itm_notes=item.notes,
            itm_imgpath=item.imgpath
        )
    def add_category(self, cat):
        self.db.add_category(
            id=cat.id,
            name=cat.name,
            notes=cat.notes
        )