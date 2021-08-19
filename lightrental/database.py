"""
LightRental database module.

All the SQL code is contained here. Other parts of
the program need not execute SQL queries - they call
methods of a class provided here. Moreover, they
shouldn't, as otherwise they can mess up the
checkin/checkout history.
"""

from PyQt5.QtSql import (
    QSqlQuery, 
    QSqlDatabase,
    QSqlRelation
)
from os import path

CHECK_IN_OUT_COLUMNS_SQL = ("id PRIMARY KEY AUTOINCREMENT,"
                "time TEXT NOT NULL,"
                "inv_nr INTEGER NOT NULL,"
                "customer_id INTEGER NOT NULL,"
                "FOREIGN KEY (inv_nr) REFERENCES inventory (inv_no)"
                " ON DELETE RESTRICT ON UPDATE CASCADE,"
                "FOREIGN KEY (customer_id) REFERENCES customers (id)"
                " ON DELETE RESTRICT ON UPDATE CASCADE,")

def open_db(filepath) -> str:
    """Opens an SQLite DB.

    :param filepath: path to an SQLite file.
    :type filepath: path
    :return: connection name (QtSQL connectionName attribute), empty if unsuccessful
    :rtype: str
    """
    name = path.basename(filepath)
    db = QSqlDatabase.addDatabase("QSQLITE", connectionName=name)
    db.setDatabaseName(filepath)
    if db.open():
        return name
    else:
        return ''

def create_db(filepath) -> str:
    """Creates an SQLite DB with a structure needed for LightRental.

    :param filepath: path and name for the new DB; if a DB exists,
    DB creation is aborted to prevent overwriting it.
    :type filepath: path
    :return: connection name (QtSQL connectionName attribute), empty if unsuccessful.
    :rtype: str
    """
    name = path.basename(filepath)
    if path.exists(filepath):
        print(f"{name} already exists. \
            DB creation aborted to prevent overwriting")
        return ""
    else:
        db = QSqlDatabase.addDatabase("QSQLITE", connectionName=name)
        db.setDatabaseName(filepath)
        if db.open():
            query = QSqlQuery(db)
            query.exec(
                "PRAGMA foreign_keys = true"
            )
            query.exec(
                "CREATE TABLE inventory ("
                "inv_nr INTEGER PRIMARY KEY ON CONFLICT ROLLBACK,"
                "sku INTEGER NOT NULL,"
                "category INTEGER NOT NULL,"
                "img_path TEXT,"
                "notes TEXT,"
                "FOREIGN KEY (sku) REFERENCES skus (sku)"
                " ON DELETE RESTRICT ON UPDATE CASCADE,"
                "FOREIGN KEY (category) REFERENCES categories (id)"
                " ON DELETE RESTRICT ON UPDATE CASCADE,"
                ")"
            )
            query.exec(
                "CREATE TABLE skus ("
                "sku INTEGER PRIMARY KEY,"
                "name TEXT NOT NULL,"
                "notes TEXT"
                ")"
            )
            query.exec(
                "CREATE TABLE categories ("
                "id INTEGER PRIMARY KEY,"
                "name TEXT NOT NULL,"
                "notes TEXT"
                ")"
            )
            query.exec(
                "CREATE TABLE customers ("
                "id PRIMARY KEY AUTOINCREMENT,"
                "name TEXT NOT NULL,"
                "contacts TEXT NOT NULL,"
                "notes TEXT"
                ")"
            )
            query.exec(
                "CREATE TABLE checkin ("
                + CHECK_IN_OUT_COLUMNS_SQL +
                ")"
            )
            query.exec(
                "CREATE TABLE checkout ("
                + CHECK_IN_OUT_COLUMNS_SQL +
                ")"
            )
            query.finish()
            return name
        else:
            return ""

class InventoryDB:
    """A database service that abstracts away the SQL under
    inventory item-specific methods.

    Note that each method obtains a fresh database handle,
    following the Qt docs' recommendation not to store the 
    handle as a member.

    The 'inventory', 'SKU' and 'categories' expose their names
    via this class' methods so that they can be directly acessed
    (and modified) by model&view objects. 
    On the contrary, records in 'checkin' and 'checkout' shouldn't 
    be ever edited or updated. One can insert records to those
    table only using this class' methods.
    """
    def __init__(self, connectionName) -> None:
        self.conn_name = connectionName
        self.inv_tbl_name = 'inventory'
        self.SKU_tbl_name = 'SKUs'
        self.cat_tbl_name = 'categories'
        self.customer_tbl_name = 'customers'
        self.index_SKU = 1
        self.index_category = 2
    def connection_handle(self):
        return QSqlDatabase.database(self.conn_name)
    def inventory_table_name(self):
        return self.inv_tbl_name
    def SKU_table_name(self):
        return self.SKU_tbl_name
    def customer_table_name(self):
        return self.customer_tbl_name
    def SKU_relation(self):
        return self.index_SKU, QSqlRelation("SKUs", "SKU", "name")
    def category_relation(self):
        return self.index_category, QSqlRelation("categories", "id", "name")
    def add_customer(self, id, name, contacts, notes=''):
        query = self._fresh_QSqlQuery()
        query.prepare(
            "INSERT INTO customers (id, name, contacts, notes) "
            "VALUES (:id, :name, :contacts, :notes)"
        )
        query.bindValue(":id", id)
        query.bindValue(":name", name)
        query.bindValue(":contacts", contacts)
        query.bindValue(":notes", notes)
        return query.exec()
    def add_item(self, nr, SKU, category, notes="", imgpath=""):
        query = self._fresh_QSqlQuery()
        query.prepare(
            "INSERT INTO inventory (inv_nr, sku, category, notes, img_path) "
            "VALUES (:inv_nr, :sku, :category, :notes, :img_path)"
        )
        query.bindValue(":sku", SKU)
        query.bindValue(":inv_nr", nr)
        query.bindValue(":category", category)
        query.bindValue(":notes", notes)
        query.bindValue(":img_path", imgpath)
        return query.exec()
    def add_SKU(self, SKU, sku_name, itm_nr, itm_cat, sku_notes='', itm_notes='', itm_imgpaths=''):
        db = self.connection_handle()
        if db.transaction():
            query = QSqlQuery(db)
            query.prepare(
                "INSERT INTO skus (sku, name, notes) "
                "VALUES (:sku, :name, :notes)"
            )
            query.bindValue(":sku", SKU)
            query.bindValue(":name", sku_name)
            query.bindValue(":notes", sku_notes)
            query.exec()
            query.prepare(
                "INSERT INTO inventory (inv_nr, sku, category, notes, img_path) "
                "VALUES (:inv_nr, :sku, :category, :notes, :img_path)"
            )
            query.bindValue(":sku", SKU)
            query.bindValue(":inv_nr", itm_nr)
            query.bindValue(":category", itm_cat)
            query.bindValue(":notes", itm_notes)
            query.bindValue(":img_path", itm_imgpaths)
            query.exec()
            db.commit()
            return True
        else:
            return False
    def add_category(self, name, notes="") -> bool:
        query = self._fresh_QSqlQuery()
        query.prepare(
            "INSERT INTO categories (name, notes) "
            "VALUES (:name, :notes)"
        )
        query.bindValue(":name", name)
        query.bindValue(":notes", notes)
        return query.exec()
    def checkin(self, nr):
        return False
    def checkout(self, nr, customer_id):
        return False
    def _fresh_QSqlQuery(self):
        db = QSqlDatabase.database(self.conn_name)
        query = QSqlQuery(db)
        return query