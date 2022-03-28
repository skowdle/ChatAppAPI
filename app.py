from flask import jsonify,Flask,request
import jsonpickle
import secrets
from datetime import datetime

app = Flask (__name__)
userinfo = []
keyinfo = {}

class Message:
    def __init__(self,user,msg):
        self.user = user
        self.msg = msg
        
class User:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.messages = []
        self.friends = []   
 
@app.route('/friend',methods=["POST"])
def user_friend():
    respkey = {}
    givenuser = request.get_json()
    if "username" not in givenuser or "loggedInUser" not in givenuser:
        respkey["success"] = "false"
        return jsonify(respkey)
    if givenuser["username"] == givenuser["loggedInUser"]:
        respkey["success"] = "false"
        return jsonify(respkey)
    for x in userinfo:
        if givenuser["username"] == x.username:
            for y in x.friends:
                if y.username == givenuser["loggedInUser"]:
                    respkey["success"] = "false"
                    return jsonify(respkey)
    for x in userinfo:
        if givenuser["username"] == x.username:
            for y in userinfo:
                if givenuser["loggedInUser"] == y.username:
                    y.friends.append(x)
                    y.messages.append([])
                    x.messages.append([])
                    x.friends.append(y)
                    respkey["success"] = "true"
                    return jsonify(respkey)
    respkey["success"] = "false"
    return jsonify(respkey)

@app.route('/message',methods=["POST"])
def get_message(): 
    respkey = {}
    count = 0
    givenuser = request.get_json()
    if "username" not in givenuser or "loggedInUser" not in givenuser:
        respkey["success"] = "false"
        return jsonify(respkey)
    for x in userinfo:
        if givenuser["username"] == x.username:
            for y in x.friends:
                if y.username == givenuser["loggedInUser"]:
                    count = 1
    if count == 1:
        for x in userinfo:
            if givenuser["username"] == x.username:
                for y in userinfo:
                    if givenuser["loggedInUser"] == y.username:
                        respkey["success"] = "true"
                        respkey["messages"] = y.messages
                        return jsonify(respkey)
    respkey["success"] = "false"
    return jsonify(respkey)
    
@app.route('/send',methods=["POST"])
def user_message(): 
    respkey = {}
    givenuser = request.get_json()
    count = 0
    flag = 0
    if "username" not in givenuser or "loggedInUser" not in givenuser or "message" not in givenuser:
        respkey["success"] = "false"
        return jsonify(respkey)
    for x in userinfo:
        if givenuser["username"] == x.username:
            for y in x.friends:
                if y.username == givenuser["loggedInUser"]:
                    flag = 1
    if flag == 1:
        for x in userinfo:
            if givenuser["username"] == x.username:
                for y in userinfo:
                    if givenuser["loggedInUser"] == y.username:
                        NewMessage = Message(givenuser["loggedInUser"], givenuser["message"])
                        y.messages[count].append(NewMessage)
                        x.messages[count].append(NewMessage)
                        respkey["success"] = "true"
                        return jsonify(respkey)
                    count += 1
    respkey["success"] = "false"
    return jsonify(respkey)
    
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
