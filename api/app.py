import configparser,  os
import time
from flask import Flask, jsonify, request

import db

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

app = Flask(__name__)
app.secret_key = "itssecret"
app.config['MONGO_URI'] = config['PROD']['DB_URI']



@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/addUser',methods=['POST'])
def addUser():
    _json = request.json
    print(_json)
    if(_json):
        return db.add_user(_json)
    else:
        return jsonify("404-wrong move")

@app.route('/api/getUsers')
def getUserList():
    return db.get_users()

if __name__ == "__main__":
    app.run(debug=True)