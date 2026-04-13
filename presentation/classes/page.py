class Page() :
    def __init__(self, last, first) -> None:
        self.actual = None
        self.last = last
        self.first = first

    def set_actual_page(self, page):
        self.actual = page
