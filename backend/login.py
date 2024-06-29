from app import app
from flask import request, jsonify, url_for
from dbse.account import *
from dbse.employee_info import *


@app.route("/login", methods=["POST"])
def login():
    user_name = request.json.get("user_name")
    pwd = request.json.get("pwd")
    if user_name is None or pwd is None:
        return jsonify({
            'response':'input none'
        })
    
    res=search_account(user_name=user_name)[0]
    if not res:
        return jsonify({
            'response': 'error user_name'
        })
    elif res != pwd:
        return jsonify({
            'response': 'error password'
        })
    else:
        return jsonify({
            'response': 'success',
            'user_id': res[0],
        })


@app.route("/register", methods=["POST"])
def register():
    user_name = request.json.get("user_name")
    password = request.json.get("pwd")
    real_name = request.json.get("real_name")
    telephone = request.json.get("telephone")
    birthday = request.json.get("birthday")
    work_experlence = request.json.get("work_experlence")

    if user_name is None or password is None:
        return jsonify({
            'response':'input none'
        })
    
    user_id = add_account(user_name, password,None)
    if user_id == 0:
        return jsonify({
            'response':'same user name'
        })
    
    add_employee_info(user_id, real_name=real_name, telephone=telephone, birthday=birthday, work_experlence=work_experlence, profile=None)
    return jsonify({
            'response':'success'
        })




    
