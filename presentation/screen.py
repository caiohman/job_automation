from PySide6 import QtWidgets
from presentation.widget import Widget
import sys
from presentation.widget_sidom_pos import WidgetSidomPos
from presentation.widget_sidom_pre import WidgetSidomPre
from presentation.classes.page import Page

class Screen():
    def __init__(self) -> None:
        page = Page(3, 1)
        app = QtWidgets.QApplication([])
        widget = QtWidgets.QStackedWidget()
        page.set_actual_page(1)
        widget.addWidget(WidgetSidomPre(widget,page))
        page.set_actual_page(2)
        widget.addWidget(Widget(widget,page))
        page.set_actual_page(3)
        widget.addWidget(WidgetSidomPos(widget, page))
        widget.resize(200,200)
        widget.show()
        sys.exit(app.exec())
