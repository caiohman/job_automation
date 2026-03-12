from PySide6 import QtCore, QtWidgets
from models.argentina import Argentina
from presentation.extration_feedback_dialog import ExtrationFeedbackDialog

class Widget(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.pdfs_directory = ""
        self.result_directory = ""

        pdfs_directory_button = QtWidgets.QPushButton("Pdfs Directory")
        pdfs_directory_button.clicked.connect(self.find_pdfs_directory)

        results_directory_button = QtWidgets.QPushButton("Results Directory")
        results_directory_button.clicked.connect(self.find_result_directory)

        extract_button = QtWidgets.QPushButton("Extract")
        extract_button.clicked.connect(self.extract)

        directories_layout = QtWidgets.QHBoxLayout()
        directories_layout.addWidget(pdfs_directory_button)
        directories_layout.addWidget(results_directory_button)

        general_layout = QtWidgets.QVBoxLayout()
        general_layout.addLayout(directories_layout)
        general_layout.addWidget(extract_button)

        self.setLayout(general_layout)

    @QtCore.Slot()
    def extract(self):
        if self.pdfs_directory != "" and self.result_directory != "":
            argentina = Argentina(self.pdfs_directory, self.result_directory)
            feedback_dialog = ExtrationFeedbackDialog(argentina.pdf_files_read_correctly, argentina.pdf_files_not_read)
            feedback_dialog.exec()

    @QtCore.Slot()
    def find_pdfs_directory(self):
        self.pdfs_directory = QtWidgets.QFileDialog.getExistingDirectory()

    @QtCore.Slot()
    def find_result_directory(self):
        self.result_directory = QtWidgets.QFileDialog.getExistingDirectory()
