from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from flask_httpauth import HTTPTokenAuth
from flask_cors import CORS, cross_origin

app = Flask(__name__)
mysql = MySQL()
auth = HTTPTokenAuth(scheme='Bearer')
CORS(app)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'flask'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['CORS_HEADERS'] = 'Content-Type'

mysql.init_app(app)

@auth.verify_token
def verify_token(token):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE token=%s", token)
    rows = cursor.fetchall()
    tok = []
    for row in rows:
        tok = row[7]
    if token == tok:
        return True
    return False

@auth.login_required
@cross_origin()
def add():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        _category_id = conn.insert_id()
        _name = request.json['name']
        _description = request.json['description']
        _quantity = request.json['quantity']
        _price = request.json['price']
        _status = request.json['status']

        if _name and _description and _quantity and _price and request.method == 'POST':
            exists = cursor.execute("SELECT * FROM products WHERE name=%s", _name)
            if not exists:
                if _status == '':
                    _status = 'Inactive'
                insert_user_cmd = "INSERT INTO products(category_id, name, description, quantity, price, status) VALUES(%s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_user_cmd, (_category_id, _name, _description, _quantity, _price, _status))
                conn.commit()
                response = jsonify(message=f'Product {_name} added successfully.', id=cursor.lastrowid)
                response.status_code = 200
            else:
                response = jsonify('400: Product already exists.')
                response.status_code = 400 
        else:
            response = jsonify('400: Some fields are empty.')
            response.status_code = 400 
    except Exception as e:
        print(e)
        response = jsonify('400: Failed to add product.')         
        response.status_code = 400 
    finally:
        cursor.close()
        conn.close()
        return(response)

@cross_origin()
@auth.login_required
def product(product_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE category_id = %s', product_id)
        rows = cursor.fetchall()
        fields = cursor.description
        column_list = []
        for i in fields:
            column_list.append(i[0])
        json = []
        for row in rows:
            data_dict = {}
            for i in range(len(column_list)):
                data_dict[column_list[i]] = row[i]
            json.append(data_dict)
        return jsonify(json)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@auth.login_required
@cross_origin()
def remove(product_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE category_id = %s', product_id)
        conn.commit()
        response = jsonify('Product deleted successfully.')
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('400: Failed to delete product.')         
        response.status_code = 400
    finally:
        cursor.close()
        conn.close()    
        return(response) 

@auth.login_required
def change(product_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        _name = request.json['name']
        _description = request.json['description']
        _quantity = request.json['quantity']
        _price = request.json['price']
        _status = request.json['status']
        update_user_cmd = "UPDATE products SET name=%s, description=%s, quantity=%s, price=%s, status=%s WHERE category_id=%s"
        cursor.execute(update_user_cmd, (_name, _description, _quantity, _price, _status, product_id))
        conn.commit()

        response = jsonify('Product updated successfully.')
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('400: Failed to update product.')         
        response.status_code = 400
    finally:
        cursor.close()
        conn.close()    
        return(response) 

@auth.login_required
@cross_origin()
def allproducts():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products;")
        rows = cursor.fetchall()
        fields = cursor.description
        column_list = []
        for i in fields:
            column_list.append(i[0])
        json = []
        for row in rows:
            data_dict = {}
            for i in range(len(column_list)):
                data_dict[column_list[i]] = row[i]
            json.append(data_dict)
        return jsonify(json)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)