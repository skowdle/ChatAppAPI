from flask import jsonify,Flask,request
import jsonpickle
import secrets
from datetime import datetime

app = Flask (__name__)
userinfo = []
keyinfo = {}

class User:
    def __init__(self,username,password):
        self.username = username
        self.password = password

User1 = User("admin","password")
userinfo.append(User1)  

    
@app.route('/login',methods=["POST"])
def user_login():
    respkey = {}
    givenuser = request.get_json()
    if "username" not in givenuser or "password" not in givenuser:
        respkey["success"] = "false"
        return jsonify(respkey)
    for x in userinfo:
        if givenuser["username"] == x.username and givenuser["password"] == x.password:
            key = secrets.token_hex(16)
            keyinfo[key] = x
            respkey["api-key"] = key
            respkey["success"] = "true"
            return jsonify(respkey)
    respkey["success"] = "false"
    return jsonify(respkey)

@app.route('/create',methods=["POST"])
def user_create():
    y = {}
    givenuser = request.get_json()
    if "username" not in givenuser or "password" not in givenuser:
        y["success"] = "false"
        return jsonify(y)
    for x in userinfo:
        if givenuser["username"] == x.username:
            y["success"] = "false"
            return jsonify(y)
    User1 = User(givenuser["username"], givenuser["password"])
    userinfo.append(User1)
    y["success"] = "true"
    return jsonify(y)
    

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)