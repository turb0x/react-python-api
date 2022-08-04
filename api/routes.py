from flask import Flask
import users
import products

app = Flask(__name__)

#users
app.add_url_rule('/api/register', view_func=users.register, methods=['POST'])
app.add_url_rule('/api/login', view_func=users.login, methods=['POST'])
app.add_url_rule('/api/change-password', view_func=users.change_password, methods=['POST'])
app.add_url_rule('/api/users/all', view_func=users.allusers, methods=['GET'])
app.add_url_rule('/api/users/<int:user_id>', view_func=users.user, methods=['GET'])
app.add_url_rule('/api/users/<int:user_id>', view_func=users.delete, methods=['DELETE'])
app.add_url_rule('/api/users/<int:user_id>', view_func=users.update, methods=['PUT'])

#products
app.add_url_rule('/api/products/add', view_func=products.add, methods=['POST'])
app.add_url_rule('/api/products/all', view_func=products.allproducts, methods=['GET'])
app.add_url_rule('/api/products/<int:product_id>', view_func=products.product, methods=['GET'])
app.add_url_rule('/api/products/<int:product_id>', view_func=products.remove, methods=['DELETE'])
app.add_url_rule('/api/products/<int:product_id>', view_func=products.change, methods=['PUT'])

if __name__ == "__main__":
    app.run(debug=True)