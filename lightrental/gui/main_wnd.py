from PyQt5.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QHBoxLayout,
    QAction
)
from PyQt5.QtGui import QKeySequence
from .checkinout_frm import CheckInFrm, CheckOutFrm
from .inventory_frm import InventoryFrm

class MainWnd(QMainWindow):
    def __init__(self) -> None:
        super(MainWnd, self).__init__()
        self._initUI()
        self._init_actions()
        self._init_menu_bar()
    def _initUI(self):
        self.main_widget = QWidget() # central widget of MainWnd's implicit layout
        layout = QHBoxLayout(self.main_widget)
        # our layout resides inside mainWidget => it'll be the parent
        self.checkin_frm = CheckInFrm()
        self.checkout_frm = CheckOutFrm()
        self.inventory_frm = InventoryFrm()
        layout.addWidget(self.checkin_frm)
        layout.addWidget(self.inventory_frm)
        layout.addWidget(self.checkout_frm)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("LightRental")
    def _init_actions(self):
        self.search_hist_action = QAction("Search in History", self)
        self.search_hist_action.setShortcut('Ctrl+H')
        self.save_history_action = QAction("Save History to a File", self)
        self.about_LR_action = QAction("About LightRental", self)
    def _init_menu_bar(self):
        menu_bar = self.menuBar()
        self.hist_menu = menu_bar.addMenu("&History")
        self.hist_menu.addAction(self.search_hist_action)
        self.hist_menu.addAction(self.save_history_action)
        self.about_menu = menu_bar.addMenu("&About")
        self.about_menu.addAction(self.about_LR_action)
    