def calculate_discount(price, discount_rate):
    total = price - (price * discount_rate)
    return total

items_in_cart = [15.50, 20.0, 9.99, 50.00]
discount = 0.15

for item in items_in_cart:
    final_price = calculate_discount(item, discount)
    print(f"The final price is: {final_price}")

# Check for high value item
if any(item > 40 for item in items_in_cart):
    print("Wow, expensive cart!")

if len(items_in_cart) > 0:
    average_price = sum(items_in_cart) / len(items_in_cart)
    print(f"Average price: {average_price}")