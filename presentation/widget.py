from PySide6 import QtCore, QtWidgets
from models.argentina import Argentina
from presentation.classes.page import Page
from presentation.extration_feedback_dialog import ExtrationFeedbackDialog

class Widget(QtWidgets.QWidget):

    def __init__(self, widget, page : Page) -> None:
        super().__init__()
        self.widget = widget
        self.page  = page
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
        general_layout.addLayout(self.createLayout())

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
