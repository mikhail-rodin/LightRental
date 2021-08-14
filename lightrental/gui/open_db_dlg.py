import sys
from functools import partial
from PyQt5.QtWidgets import (
    QDialog,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
)

class OpenDatabaseDialog(QDialog):
    """Dialog shown at startup where an SQLite db file is chosen
    """
    def __init__(self, recent=None) -> None:
        """Dialog optionally initialized with a list of recent SQLite files

        :param recent: recent SQLite db file locations, defaults to None
        :type recent: list, optional
        """
        super().__init__()
        self.init_widgets()
        self.connect_slots()
        if recent is not None:
            for fname in recent:
                QListWidgetItem(fname, self.db_list)
        self.selected_fname=''
        self.connect_btn.setEnabled(False)
    def init_widgets(self):
        lay = QVBoxLayout()
        self.navigate_btn = QPushButton("Navigate")
        self.db_list = QListWidget()
        self.db_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.connect_btn = QPushButton("Connect")
        lay.addWidget(self.navigate_btn)
        lay.addWidget(self.db_list)
        lay.addWidget(self.connect_btn)
        self.setLayout(lay)
    def connect_slots(self):
        self.navigate_btn.clicked.connect(self.on_open_file)
        self.connect_btn.clicked.connect(self.on_accept)
        self.db_list.itemSelectionChanged.connect(partial(self.connect_btn.setEnabled, True))  
    def on_open_file(self):
        filename, _filter = QFileDialog.getOpenFileName(
            parent = self,
            caption = "Open SQLite file",
            directory = '',
            filter="SQLite Database (*.sqlite)"
        )
        if not filename == '':
            QListWidgetItem(filename, parent=self.db_list)
    def on_accept(self):
        self.selected_fname = self.db_list.selectedItems()[0]
        super().accept()
    def get_filename(self):
        return self.selected_fname
    def closeEvent(self, event):
        """Close the entire app.

        TODO: properly exit without leaving any dangling memory

        :param event: [description]
        :type event: [type]
        """
        sys.exit(0)