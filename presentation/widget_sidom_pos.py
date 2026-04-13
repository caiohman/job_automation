from PySide6 import QtCore, QtWidgets
from presentation.classes.page import Page
from presentation.components.login_dialog import LoginDialog

class WidgetSidomPos(QtWidgets.QWidget):
    def __init__(self, widget, page : Page) -> None:
        super().__init__()
        self.widget = widget
        self.page  = page

        login_button = QtWidgets.QPushButton("Sidom Login")
        login_button.clicked.connect(self.login)

        general_layout = QtWidgets.QVBoxLayout()
        general_layout.addWidget(login_button)
        general_layout.addLayout(self.createLayout())

        self.setLayout(general_layout)

    @QtCore.Slot()
    def login(self):
        login_dialog = LoginDialog()
        login_dialog.exec()

    def create_back_button(self):
        back_button = QtWidgets.QPushButton()
        back_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowBack))
        back_button.setFixedSize(30, 30)
        back_button.clicked.connect(self.change_down)
        back_button.setEnabled(False) if self.page.actual == self.page.first else back_button.setEnabled(True)
        return back_button

    def create_forward_button(self):
        forward_button = QtWidgets.QPushButton()
        forward_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowForward))
        forward_button.setFixedSize(30, 30)
        forward_button.clicked.connect(self.change_up)
        forward_button.setEnabled(False) if self.page.actual == self.page.last else forward_button.setEnabled(True)
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
