class Book:
    def __init__(
        self,
        book_id,
        ISBN,
        name,
        author,
        author_original,
        translator,
        publishing_house,
        publishing_date,
        price,
        discount_price,
        expire_date,
    ):
        self.book_id = book_id
        self.ISBN = ISBN
        self.name = name
        self.author = author
        self.author_original = author_original
        self.translator = translator
        self.publishing_house = publishing_house
        self.publishing_date = publishing_date
        self.price = price
        self.discount_price = discount_price
        self.expire_date = expire_date

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "ISBN": self.ISBN,
            "name": self.name,
            "author": self.author,
            "author_original": self.author_original,
            "translator": self.translator,
            "publishing_house": self.publishing_house,
            "publishing_date": self.publishing_date,
            "price": self.price,
            "discount_price": self.discount_price,
            "expire_date": self.expire_date,
        }
