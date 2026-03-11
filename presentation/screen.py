from PySide6 import QtWidgets
from presentation.widget import Widget
import sys

class Screen():

    def __init__(self) -> None:
        app = QtWidgets.QApplication([])
        widget = Widget()
        widget.resize(200,200)
        widget.show()
        sys.exit(app.exec())
