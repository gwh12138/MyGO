from app import app
from flask import request, jsonify, url_for
from dbse.account import *


@app.route("/login", methods=["POST"])
def login():
    user_id = request.json.get("user_id")
    pwd = request.json.get("pwd")
    if user_id is None or pwd is None:
        return jsonify({
            'response':'input none'
        })
    
    search_account(user_id=user_id)
    


    
