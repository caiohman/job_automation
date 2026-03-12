from PySide6 import QtCore, QtWidgets


class ExtrationFeedbackDialog(QtWidgets.QDialog):
    def __init__(self, pdf_files_read_correctly, pdf_files_not_read) -> None:
        super().__init__()

        pdf_files_read_correctly_dropdown = QtWidgets.QComboBox()
        pdf_files_read_correctly_dropdown.addItem('Extrated')
        pdf_files_read_correctly_dropdown.addItems(pdf_files_read_correctly)
        pdf_files_not_read_dropdown = QtWidgets.QComboBox()
        pdf_files_not_read_dropdown.addItem('Not Extracted')
        pdf_files_not_read_dropdown.addItems(pdf_files_not_read)

        files_list = QtWidgets.QHBoxLayout()
        files_list.addWidget(pdf_files_read_correctly_dropdown)
        files_list.addWidget(pdf_files_not_read_dropdown)

        general_layout = QtWidgets.QVBoxLayout()
        general_layout.addLayout(files_list)
        self.setLayout(general_layout)
