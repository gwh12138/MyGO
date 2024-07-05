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
    
    res=search_account(user_name=user_name)
    if not res:
        return jsonify({
            'response': 'error user_name'
        })
    res = res[0]
    if res[2] != pwd:
        return jsonify({
            'response': 'error password'
        })
    else:
        return jsonify({
            'response': 'success',
            'user_id': res[0],
            'role': res[3],
        })


@app.route("/register", methods=["POST"])
def register():
    user_name = request.json.get("user_name")
    password = request.json.get("pwd")
    role = request.json.get("role")
    real_name = request.json.get("real_name")
    telephone = request.json.get("telephone")
    birthday = request.json.get("birthday")
    work_experience = request.json.get("work_experience")

    if user_name is None or password is None:
        return jsonify({
            'response':'input none'
        })
    if len(user_name) < 3:
        return jsonify({
            'response': 'user name too short'
        })
    if len(password) < 3:
        return jsonify({
            'response': 'password too short'
        })
    user_id = add_account(user_name, password, role)
    if user_id is None:
        return jsonify({
            'response':'500'
        })
    elif user_id == 0:
        return jsonify({
            'response':'same user name'
        })
    
    add_employee_info(user_id, real_name=real_name, telephone=telephone, birthday=birthday, work_experience=work_experience, profile=None)
    return jsonify({
            'response':'success'
        })




    
