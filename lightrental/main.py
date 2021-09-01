import argparse
from .gui.open_db_dlg import OpenDatabaseDialog
from .gui.main_wnd import MainWnd
from .database import InventoryDB, open_db, create_db
from .datamodel import InventoryModel
import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox

def main():
    """Main, not the entry point. Contains two event loops and arg parsing.

    The 1st event loop is started with the database selection dialog.
    Then a data model is created from a DB.
    Finally the model is passed to the GUI and the 2nd (main) event loop starts. 
    """
    ap = argparse.ArgumentParser(
        prog='LightRental 0.1.0',
        description="LightRental is a dual interface GUI/CLI utility for keeping \
            track of a rental inventory"
    )
    setup_argparser(ap)
    args = ap.parse_args()
    if args.gui:
    # mode 1/3: working with an existing DB via GUI
        app = QApplication(sys.argv)
        if not args.db_filepath:
            open_dlg = OpenDatabaseDialog()
            if open_dlg.exec(): #a modal dialog runs its own event loop
                conn_name = open_db(open_dlg.get_filename())
        else: conn_name = open_db(args.db_filepath)
        if conn_name == '':
            pass 
            QMessageBox.critical(
                parent=None,
                title="Error",
                text="open_db(db) : could not establish connection to database."
            )
        else:
            main_wnd = MainWnd(InventoryModel(InventoryDB(conn_name)))
            main_wnd.show()
            sys.exit(app.exec())
    elif args.new_db:
    # mode 2/3: administration, creating a db
        path = args.db_filepath if args.db_filepath else os.getcwd()
        conn_name = create_db_session(path) 
        if not conn_name == '':
            interactive_session(InventoryDB(conn_name))
    else:
    # mode 3/3: interactive CLI
        if not args.db_filepath:
            while True:
                path_input = input("Enter path to database: ")
                if os.path.exists(path_input):
                    conn_name = open_db(path_input)
                    if conn_name == '':
                        print("Error: sqlite driver couldn't open the file provided by you.")
                    else:
                        break
                else:
                    print("Error: Invalid path. Try again.")
        else:
            conn_name = open_db(args.db_filepath)
            if conn_name == '':
                print("Error: sqlite driver couldn't open the file provided by you.")
        interactive_session(InventoryDB(conn_name))
    sys.exit(0)

def setup_argparser(parser):
    parser.add_argument(
        "--file",
        "-f",
        required=False,
        dest='db_filepath',
        help="SQLite3 database file"
    )
    parser.add_argument(
        "--gui",
        "-g",
        required=False,
        action="store_true",
        dest="gui",
        help="Start with a graphical interface."
    )
    parser.add_argument(
        "--new-db",
        "-n",
        dest="new_db",
        help="Create a new database."
    )
def interactive_session(db):
    while True:
        # at each iteration defaults are loaded
        # so that the previous one won't corrupt the queries
        name = ''
        sku = -1
        cat = -1
        notes = ''

        cmd = input(">")
        action = cmd.split(" ")[0]
        action_obj = cmd.split(" ")[1]
        if action in ['help', 'h']:
            print(
                """Actions:
                'add',      'a'  [itm, sku, cat]
                'del',      'd'  [cat]
                'checkin',  'ci' [itm]
                'checkout', 'co' [itm]
                'exit'
                """
            )
        elif action in ['exit', 'e', 'quit', 'q']:
            break # end event loop
        elif action in ['add', 'a']:
            if action_obj in ['itm', 'i']:
                print("You're adding an item to an existing SKU.")
                sku = input('SKU: ')
                cat = input('Category (id or name: ')
                notes = input('Notes (hit Enter if none): ')
            elif action_obj in ['sku', 's']:
                print("You're adding a new SKU. \
                    You'll be asked to provide the first item too, \
                    as SKU's can't be empty")
            elif action_obj in ['cat', 'c']:
                pass
        elif action in ['del', 'd']:
            if action_obj in ['itm', 'i', 'sku', 's']:
                print("Deletion of items and SKUs not allowed \
                    for the sake of transaction history integrity. \
                    (Otherwise dangling item references could appear)")
            elif action_obj in ['cat', 'c']:
                pass
        elif action in ['checkin', 'ci']:
            inv_no = input("Inv. number: ")
            db.checkin(inv_no)
        elif action in ['checkout', 'co']:
            pass
def create_db_session(path) -> str:
    print(f"Attempting to create a new database at {path}")
    if input("Create new database? (y/n)") == 'y':
        conn_name = create_db(path)
        if conn_name == '':
            print("Error: create_db(filepath) failed, SQLite transaction rolled back, no db structure created.")
        else:
            print(f"DB structure initialized, connection name: {conn_name}")
            return conn_name
    return ''