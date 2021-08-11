from PyQt5.QtWidgets import QWidget, QGridLayout, QTableView, QComboBox, QLineEdit, QPushButton
class CheckInOutFrm(QWidget):
    """Base class for Checkin and Checkout forms.

    Holds widgets that appear in both. 
    """

    def __init__(self, frm_name="", parent=None) -> None:
        """Creates a QWidget and delegates creating widgets to init_widgets

        :param frm_name: Caption that'll appear on buttons & labels; 
        tells what the form is doing to the database.
        :type frm_name: str
        :param parent: Parent QObject that gets passed to the base class QWidget
        """
        
        super().__init__(parent)
        self.layout = self.init_widgets(frm_name)
    def init_widgets(self, frm_name):
        """Draws widgets
        
        :param frm_name: Button & label caption: what the form is doing
        :type frm_name: str
        """
        lay = QGridLayout(self)
        inv_no_input = QLineEdit()
        inv_no_enter = QPushButton(frm_name)
        hist_view = QTableView()
        #addWidget(widget: QWidget, row: int, col: int, [rowSpan, colSpan, alignment])
        lay.addWidget(inv_no_input, 1, 0)
        lay.addWidget(inv_no_enter, 1, 1)
        lay.addWidget(hist_view, 2, 0, 1, 2)
        return lay

class CheckInFrm(CheckInOutFrm):
    def __init__(self, parent=None) -> None:
        CheckInOutFrm.__init__(self, frm_name="Checkin")
class CheckOutFrm(CheckInOutFrm):
    def __init__(self, parent=None) -> None:
        CheckInOutFrm.__init__(self, frm_name="Checkout")
        client_selector = QComboBox()
        self.layout.addWidget(client_selector, 0, 0, 1, 2)
        #lay.addWidget(client_selector, 0, 0)