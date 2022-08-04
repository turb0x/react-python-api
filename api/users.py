from secrets import token_urlsafe
from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from flask_bcrypt import Bcrypt
import datetime
from flask_httpauth import HTTPTokenAuth
from flask_cors import CORS, cross_origin


app = Flask(__name__)
mysql = MySQL()
bcrypt = Bcrypt(app)
auth = HTTPTokenAuth(scheme='Bearer')
CORS(app)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'flask'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['CORS_HEADERS'] = 'Content-Type'

mysql.init_app(app)

@cross_origin()
def register():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        _id = conn.insert_id()
        _name = request.json['name']
        _email = request.json['email']
        _password = request.json['password']
        _password_confirmation = request.json['password_confirmation']
        _created_at = str(datetime.datetime.now())
        _updated_at = str(datetime.datetime.now())
        _last_login = str(datetime.datetime.now())
        _token = str(token_urlsafe(20))

        if _name and _email and _password and _password_confirmation and request.method == 'POST':
            exists = cursor.execute("SELECT * FROM users WHERE email=%s", _email)
            if not exists:
                if _password == _password_confirmation:
                    _hashed = bcrypt.generate_password_hash(_password).decode('utf-8')
                    insert_user_cmd = "INSERT INTO users(id, name, email, password, created_at, updated_at, last_login, token) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(insert_user_cmd, (_id, _name, _email, _hashed, _created_at, _updated_at, _last_login, _token))
                    conn.commit()
                    response = jsonify(message=f'User {_name} added successfully.', id=cursor.lastrowid, token=_token, last_login=_last_login)
                    response.status_code = 200
                else:
                    response = jsonify('400: The passwords are not matching.')
                    response.status_code = 400 
            else:
                response = jsonify('400: Email already exists.')
                response.status_code = 400 
        else:
            response = jsonify('400: Some fields are empty.')
            response.status_code = 400 
    except Exception as e:
        print(e)
        response = jsonify('400: Failed to add user.')         
        response.status_code = 400 
    finally:
        cursor.close()
        conn.close()
        return(response)

@cross_origin()
def login():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        _email = request.json['email']
        _password = request.json['password']
        _last_login = str(datetime.datetime.now())
        _token = str(token_urlsafe(20))

        if _email and _password and request.method == 'POST':
            cursor.execute("SELECT password FROM users WHERE email=%s", _email)
            rows = cursor.fetchall()
            for row in rows:
                hashed = row[0]
            checked = bcrypt.check_password_hash(hashed, _password)
            if checked:
                update_user_cmd = "UPDATE users SET last_login=%s, token=%s WHERE email=%s"
                cursor.execute(update_user_cmd, (_last_login, _token, _email))
                conn.commit()
                response = jsonify(message=f'Welcome back!', token=_token, last_login=_last_login)
                response.status_code = 200
            else:
                response = jsonify('400: Wrong email or password.')
                response.status_code = 400 
        else:
            response = jsonify('400: Some fields are empty.')
            response.status_code = 400 
    except Exception as e:
        print(e)
        response = jsonify('400: Failed to log in.')         
        response.status_code = 400 
    finally:
        cursor.close()
        conn.close()
        return(response)

def change_password():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        _email = request.json['email']
        _old_password = request.json['old_password']
        _new_password = request.json['new_password']
        _new_password_confirmation = request.json['new_password_confirmation']
        _updated_at = str(datetime.datetime.now())
        if _email and _old_password and _new_password and _new_password_confirmation and request.method == 'POST':   
            cursor.execute("SELECT password FROM users WHERE email=%s", _email)
            rows = cursor.fetchall()
            for row in rows:
                hashed = row[0]
            checked = bcrypt.check_password_hash(hashed, _old_password)
            if checked:
                if _new_password == _new_password_confirmation:
                    _hashed = bcrypt.generate_password_hash(_new_password).decode('utf-8')
                    updated_pass = "UPDATE users SET password=%s, updated_at=%s WHERE email=%s"
                    cursor.execute(updated_pass, (_hashed, _updated_at, _email))
                    conn.commit()
                    response = jsonify(message=f'Password updated!', updated_at=_updated_at)
                    response.status_code = 200
                else:
                    response = jsonify('400: The passwords are not matching.')
                    response.status_code = 400 
            else:
                response = jsonify('400: Wrong old password.')
                response.status_code = 400 
        else:
            response = jsonify('400: Wrong email or password.')
            response.status_code = 400 
    except Exception as e:
        print(e)
        response = jsonify('400: Failed to change the password.')         
        response.status_code = 400
    finally:
        cursor.close()
        conn.close()    
        return(response)       

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
def allusers():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users;")
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
def user(user_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', user_id)
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
def delete(user_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = %s',user_id)
        conn.commit()
        response = jsonify('User deleted successfully.')
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('400: Failed to delete user.')         
        response.status_code = 400
    finally:
        cursor.close()
        conn.close()    
        return(response)    

@auth.login_required
def update(user_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        _name = request.json['name']
        _email = request.json['email']
        _updated_at = str(datetime.datetime.now())
        update_user_cmd = "UPDATE users SET name=%s, email=%s, updated_at=%s WHERE id=%s"
        cursor.execute(update_user_cmd, (_name, _email, _updated_at, user_id))
        conn.commit()

        response = jsonify('User updated successfully.')
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('400: Failed to update user.')         
        response.status_code = 400
    finally:
        cursor.close()
        conn.close()    
        return(response)       

if __name__ == "__main__":
    app.run(debug=True)