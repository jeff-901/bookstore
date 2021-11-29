class Order:
    def __init__(self, order_id, total_price, time, items):
        self.order_id = order_id
        self.total_price = total_price
        self.time = time
        self.items = []
        for item in items:
            self.items.append(
                {"book_id": item.book_id, "number": item.number, "price": item.price}
            )

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "total_price": self.total_price,
            "time": self.time,
            "items": self.items,
        }
