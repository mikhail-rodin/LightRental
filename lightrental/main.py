from .gui.open_db_dlg import OpenDatabaseDialog
from .gui.main_wnd import MainWnd
import sys
from PyQt5.QtWidgets import QApplication

def main():
    """Main, not the entry point. Contains two event loops and arg parsing.

    The 1st event loop is started with the database selection dialog.
    Then a data model is created from a DB.
    Finally the model is passed to the GUI and the 2nd (main) event loop starts. 
    """
    app = QApplication(sys.argv)
    open_dlg = OpenDatabaseDialog()
    if open_dlg.exec(): #a modal dialog runs its own event loop
        main_wnd = MainWnd()
        main_wnd.show()
    sys.exit(app.exec())