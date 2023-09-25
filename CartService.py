from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Sample cart data (for demonstration purposes)
carts = {}

# Endpoint to retrieve the current contents of a user's shopping cart
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    if user_id in carts:
        user_cart = carts[user_id]
        return jsonify(user_cart)
    else:
        return jsonify({"error": "Cart not found"}), 404

# Endpoint to add a specified quantity of a product to the user's cart
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    data = request.get_json()
    quantity = data.get("quantity", 1)

    # Retrieve product details from the Product Service
    product_response = requests.get(f"http://localhost:5000/products/{product_id}")
    if product_response.status_code != 200:
        return jsonify({"error": "Product not found"}), 404

    product = product_response.json()

    # Update the user's cart
    if user_id in carts:
        user_cart = carts[user_id]
    else:
        user_cart = {}
    
    if product_id in user_cart:
        user_cart[product_id]["quantity"] += quantity
    else:
        user_cart[product_id] = {
            "name": product["name"],
            "quantity": quantity,
            "total_price": quantity * product["price"]
        }

    carts[user_id] = user_cart

    return jsonify(user_cart), 201

# Endpoint to remove a specified quantity of a product from the user's cart
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    data = request.get_json()
    quantity = data.get("quantity", 1)

    if user_id in carts and product_id in carts[user_id]:
        user_cart = carts[user_id]
        if user_cart[product_id]["quantity"] >= quantity:
            user_cart[product_id]["quantity"] -= quantity
            user_cart[product_id]["total_price"] -= quantity * user_cart[product_id]["total_price"]

            if user_cart[product_id]["quantity"] == 0:
                del user_cart[product_id]

            return jsonify(user_cart), 200
        else:
            return jsonify({"error": "Not enough quantity in the cart"}), 400
    else:
        return jsonify({"error": "Product not found in the cart"}), 404

if __name__ == '__main__':
    app.run(debug=True)
