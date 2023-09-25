from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample product data (for demonstration purposes)
products = [
    {"id": 1, "name": "Apple", "price": 1.0, "quantity": 100},
    {"id": 2, "name": "Banana", "price": 0.5, "quantity": 150},
    {"id": 3, "name": "Orange", "price": 0.75, "quantity": 120},
]

# Endpoint to retrieve a list of available grocery products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

# Endpoint to get details about a specific product by its unique ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({"error": "Product not found"}), 404

# Endpoint to add new grocery products to the inventory
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    if not all(key in data for key in ["name", "price", "quantity"]):
        return jsonify({"error": "Missing data"}), 400
    
    new_id = max([p["id"] for p in products]) + 1
    new_product = {
        "id": new_id,
        "name": data["name"],
        "price": data["price"],
        "quantity": data["quantity"]
    }
    products.append(new_product)
    
    return jsonify(new_product), 201

if __name__ == '__main__':
    app.run(debug=True)
