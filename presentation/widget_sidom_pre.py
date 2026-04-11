from PySide6 import QtCore, QtWidgets
from presentation.components.login_dialog import LoginDialog

class WidgetSidomPre(QtWidgets.QWidget):
    def __init__(self, widget, actual_page, last_page, first_page) -> None:
        super().__init__()

        self.widget = widget
        self.actual_page = actual_page
        self.first_page = first_page
        self.last_page = last_page

        self.process_chosen_index = None
        self.country_chosen_index = None

        country_button = QtWidgets.QComboBox()
        country_button.setPlaceholderText("choose country")
        country_button.addItems(self.country_names(None))
        country_button.activated.connect(self.country_chosen)

        process_button = QtWidgets.QComboBox()
        process_button.setPlaceholderText("choose process")
        process_button.addItems(self.process_names(None))
        process_button.activated.connect(self.process_chosen)

        login_button = QtWidgets.QPushButton("Sidom Login")
        login_button.clicked.connect(self.login)

        options_layout = QtWidgets.QHBoxLayout()
        options_layout.addWidget(country_button)
        options_layout.addWidget(process_button)

        general_layout = QtWidgets.QVBoxLayout()
        general_layout.addLayout(options_layout)
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
        if self.process_chosen_index is not None and self.country_chosen_index is not None :
            login_dialog = LoginDialog()
            login_dialog.get_country_process(self.country_names(self.country_chosen_index), self.process_names(self.process_chosen_index))
            login_dialog.exec()

    def country_names(self, index):
        countries = ["Argentina", "Paraguai", "Chile", "Bolivia"]
        if index is None:
            return countries
        else:
            return countries[index]

    def process_names(self, index):
        processes = ["Destination", "Vendor", "Broker"]
        if index is None:
            return processes
        else:
            return processes[index]

    @QtCore.Slot()
    def country_chosen(self, result):
        self.country_chosen_index = int(result)

    @QtCore.Slot()
    def process_chosen(self, result):
        self.process_chosen_index = int(result)
