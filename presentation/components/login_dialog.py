from PySide6 import QtCore, QtWidgets


class LoginDialog(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()

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
        print(self.user_input.text())
        print(self.password_input.text())
