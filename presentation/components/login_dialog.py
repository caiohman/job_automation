from PySide6 import QtCore, QtWidgets
from sidom.sidom import Sidom

class LoginDialog(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.country = None
        self.process = None

        user = QtWidgets.QLabel("Username")
        self.user_input = QtWidgets.QLineEdit()

        password = QtWidgets.QLabel("Password")
        self.password_input = QtWidgets.QLineEdit(echoMode = QtWidgets.QLineEdit.EchoMode.Password)

        submit_button = QtWidgets.QPushButton("Submit")
        submit_button.clicked.connect(self.submit)

        general_layout = QtWidgets.QGridLayout()
        general_layout.addWidget(user, 1, 0)
        general_layout.addWidget(self.user_input, 1, 1)
        general_layout.addWidget(password, 2, 0)
        general_layout.addWidget(self.password_input, 2, 1)
        general_layout.addWidget(submit_button, 3, 0, 1, 2)
        self.setLayout(general_layout)

    @QtCore.Slot()
    def submit(self):
        username = self.user_input.text()
        password = self.password_input.text()

        if username != '' and password != '':
            sidom = Sidom(username, password)

            if self.country is not None and self.process is not None :
                sidom.get_cases(self.country, self.process)

            sidom.connection()

    def get_country_process(self, country, process):
        self.country = country
        self.process = process
