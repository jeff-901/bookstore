class User:
    def __init__(
        self,
        user_id,
        role,
        first_name,
        last_name,
        email,
        phone,
        gender,
        address,
        cart,
        orders,
    ):
        self.user_id = user_id
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.gender = gender
        self.address = address
        self.cart = [cart_item.to_entity().to_dict() for cart_item in cart] or []
        self.orders = [order.to_entity().to_dict() for order in orders] or []
