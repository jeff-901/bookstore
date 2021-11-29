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
        self.orders = [order.order_id for order in orders] or []

    # def user_id(self):
    #     return self.user_id

    # def role(self):
    #     return self.role

    # def first_name(self):
    #     return self.first_name

    # def last_name(self):
    #     return self.last_name

    # def email(self):
    #     return self.email

    # def phone(self):
    #     return self.phone

    # def gender(self):
    #     return self.gender

    # def address(self):
    #     return self.address

    # def cart(self):
    #     return self.cart

    # def orders(self):
    #     return self.orders

    # def serialize(self):
    #     return {
    #         "user_id": self.user_id,
    #         "role": self.role,
    #         "first_name": self.first_name,
    #         "last_name": self.last_name,
    #         "email": self.email,
    #         "phone": self.phone,
    #         "gender": self.gender,
    #         "address": self.address,
    #         "cart": self.cart,
    #         "orders": self.orders,
    #     }
