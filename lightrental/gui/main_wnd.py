from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from .checkinout_frm import CheckInFrm

class MainWnd(QMainWindow):
    def __init__(self) -> None:
        super(MainWnd, self).__init__()
        self.initUI()
    def initUI(self):
        self.main_widget = QWidget() # central widget of MainWnd's implicit layout
        layout = QHBoxLayout(self.main_widget)
        # our layout resides inside mainWidget => it'll be the parent
        checkin_frm = CheckInFrm(self.main_widget)
        layout.addWidget(checkin_frm)
        self.setCentralWidget(self.main_widget)