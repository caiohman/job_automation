from PySide6 import QtCore, QtWidgets
from presentation.components.login_dialog import LoginDialog
from sidom.sidom import Sidom

class WidgetSidomPre(QtWidgets.QWidget):
    def __init__(self, widget, actual_page, last_page, first_page) -> None:
        super().__init__()

        self.widget = widget
        self.actual_page = actual_page
        self.first_page = first_page
        self.last_page = last_page

        login_button = QtWidgets.QPushButton("Sidom Login")
        login_button.clicked.connect(self.login)

        general_layout = QtWidgets.QVBoxLayout()
        general_layout.addWidget(login_button)
        general_layout.addLayout(self.createLayout())

        self.setLayout(general_layout)

    def create_back_button(self):
        back_button = QtWidgets.QPushButton()
        back_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowBack))
        back_button.setFixedSize(30, 30)
        back_button.clicked.connect(self.change_down)
        back_button.setEnabled(False) if self.actual_page == self.first_page else back_button.setEnabled(True)
        return back_button

    def create_forward_button(self):
        forward_button = QtWidgets.QPushButton()
        forward_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowForward))
        forward_button.setFixedSize(30, 30)
        forward_button.clicked.connect(self.change_up)
        forward_button.setEnabled(False) if self.actual_page == self.last_page else forward_button.setEnabled(True)
        return forward_button

    def createLayout(self):
        changeLayout = QtWidgets.QHBoxLayout()
        changeLayout.addWidget(self.create_back_button())
        changeLayout.addWidget(self.create_forward_button())
        return changeLayout

    @QtCore.Slot()
    def change_up(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    @QtCore.Slot()
    def change_down(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() - 1)

    @QtCore.Slot()
    def login(self):
        login_dialog = LoginDialog()
        login_dialog.exec()
