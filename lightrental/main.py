from .gui.main_wnd import MainWnd
import sys
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    main_wnd = MainWnd()
    main_wnd.show()
    sys.exit(app.exec())