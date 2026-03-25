from PySide6 import QtWidgets
from presentation.widget import Widget
import sys
from presentation.widget_sidom_pos import WidgetSidomPos
from presentation.widget_sidom_pre import WidgetSidomPre

class Screen():
    def __init__(self) -> None:
        first_page = 1
        last_page = 3

        app = QtWidgets.QApplication([])
        widget = QtWidgets.QStackedWidget()
        widget.addWidget(WidgetSidomPre(widget, actual_page=1, last_page=last_page, first_page=first_page))
        widget.addWidget(Widget(widget, actual_page=2, last_page=last_page, first_page=first_page))
        widget.addWidget(WidgetSidomPos(widget, actual_page=3, last_page=last_page, first_page=first_page))
        widget.resize(200,200)
        widget.show()
        sys.exit(app.exec())
