from cryptography.fernet import Fernet
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import sqlite3
import os
from datetime import timedelta


def generateKey():
    key = Fernet.generate_key()
    with open('cryptkey.key', 'wb') as key_file:
        key_file.write(key)

def loadKey():
    with open("cryptkey.key", "rb") as key_file:
        return key_file.read()

def encryptPass(password):
    key = loadKey()
    cipher = Fernet(key)
    encryptedPass = cipher.encrypt(password.encode())
    return encryptedPass

def decryptPass(encryptedPass):
    key = loadKey()
    cipher = Fernet(key)
    decryptedPass = cipher.decrypt(encryptedPass).decode()
    return decryptedPass

def connectToSQL(name):
    return sqlite3.connect(name)

def connectCursor(connection):
    return connection.cursor()


app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'test'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
jwt = JWTManager(app)

@app.route("/login", methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username == 'test' and password == 'testy':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    else:
        return jsonify({'msg': 'Wrong username or password'}), 401


@app.route("/saveCredentials", methods=['POST'])
@jwt_required()
def saveCredentials():
    connection = connectToSQL("logins.db")
    cursor = connectCursor(connection)

    data = request.get_json()
    website = data['host']
    username = data['username']
    password = encryptPass(data['password'])

    cursor.execute("INSERT INTO Logins VALUES (?, ?, ?)", (website, username, password))
    connection.commit()

    cursor.close()
    connection.close()
    return jsonify({"response": "Saved Password"})

@app.route("/removePass", methods=['POST'])
@jwt_required()
def removePass():
    connection = connectToSQL("logins.db")
    cursor = connectCursor(connection)

    url = request.json.get('url')
    cursor.execute("DELETE FROM Logins WHERE Website=?", (url,))
    connection.commit()

    cursor.close()
    connection.close()
    return jsonify({"response": "Password removed"})

@app.route("/searchUsername", methods=['POST', 'GET'])
@jwt_required()
def searchUsername():
    connection = connectToSQL("logins.db")
    cursor = connectCursor(connection)

    url = request.data.decode().strip('"')
    cursor.execute("SELECT * FROM Logins WHERE Website=?", (url,))
    data = cursor.fetchone()

    cursor.close()
    connection.close()

    if data is None:
        return jsonify({"Error": "No credentials found"}), 404
    else:
        return jsonify({
            "website": data[0],
            "username": data[1]
        })

@app.route("/searchPass", methods=['POST', 'GET'])
@jwt_required()
def searchPass():
    connection = connectToSQL("logins.db")
    cursor = connectCursor(connection)

    url = request.data.decode().strip('"')
    cursor.execute("SELECT * FROM Logins WHERE Website=?", (url,))
    data = cursor.fetchone()

    cursor.close()
    connection.close()

    if data is None:
        return jsonify({"Error": "No credentials found"}), 404
    else:
        return jsonify({
            "website": data[0],
            "password": decryptPass(data[2])  # Decrypt the password before sending it back
        })

if __name__ == "__main__":
    if not os.path.isfile("./logins.db"):
        with open("./createDatabase.py") as file:
            exec(file.read())

    if not os.path.isfile("./cryptkey.key"):
        generateKey()

    app.run(host="0.0.0.0", port=80, debug=True)
