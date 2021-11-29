class CartWithBook:
    def __init__(self, cart, book):
        self.book_id = cart.book_id
        self.number = cart.number
        self.book = book

    def to_dict(self):
        return {"book_id": self.book_id, "number": self.number, "book": self.book}
