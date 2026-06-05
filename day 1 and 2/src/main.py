from models import Customer, Product, Order
from exceptions import validate_age

customer = Customer(
    "Kanishk",
    "kanishksb2005@gmail.com",
    100
)

product = Product("Laptop", 50000)

order = Order(customer, product)

print(customer.display())
print(order.total())

try:
    validate_age(15)

except Exception as e:
    print(e)

finally:
    print("Program completed")