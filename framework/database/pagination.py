import math


class Pagination:

    def __init__(self, page: int = 1, page_size: int = 10):
        self.page = page
        self.page_size = page_size
        self.total_objects = 0

    @property
    def start(self):
        return self.page - 1

    @property
    def skip(self):
        return self.page_size * self.start

    @property
    def pages(self):
        return math.ceil(self.total_objects / self.page_size)

    def result(self):  # sourcery skip: simplify-numeric-comparison
        return {
            "pages": self.pages,
            "per_page": self.page_size,
            "next_page_number": self.page + 1 if self.pages >= (self.page + 1) else None,
            "previous_page_number": self.page - 1 if self.page - 1 > 0 else None,
            "total_objects": self.total_objects
        }
