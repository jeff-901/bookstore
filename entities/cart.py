class Cart:
    def __init__(self, book_id, number):
        self.book_id = book_id
        self.number = number

    def to_dict(self):
        return {"book_id": self.book_id, "number": self.number}
