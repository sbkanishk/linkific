class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def display(self) -> str:
        return f"{self.name} - {self.email}"


class Customer(User):
    def __init__(self, name: str, email: str, points: int):
        super().__init__(name, email)
        self.points = points

    def display(self) -> str:
        return f"{super().display()} | Points: {self.points}"


class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


class Order:
    def __init__(self, customer: Customer, product: Product):
        self.customer = customer
        self.product = product

    def total(self) -> float:
        return self.product.price