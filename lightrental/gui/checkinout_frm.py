from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView
class CheckInOutFrm(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.initWidgets()
    def initWidgets(self):
        layout = QVBoxLayout(self)
        hist_view = QTableView()
        layout.addWidget(hist_view)

class CheckInFrm(CheckInOutFrm):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)