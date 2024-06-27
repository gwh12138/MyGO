from run import app
import flask
import re
from flask import request, jsonify, url_for
from dbapi import *
import dbapi as db


@app.route("/login", methods=["POST"])
def login():
    user_name = request.json.get("user_name")
    pwd = request.json.get("pwd")
    role_in = request.json.get("role")
    if user_name is None or pwd is None:
        return jsonify({
            'response':'input none'
        })

    # user_name = re.search(r"^(?=.*[a-zA-Z])(?=.*\d).{1,10}$", user_name)
    # pwd = re.search(r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@#$%^&+=!])(?!.*\s).{1,10}$", pwd)
    if user_name is None or pwd is None:
        return jsonify({
            'response': 'input illegal'
        })

    (user_id, role) = get_account(user_name, pwd)
    if None in (user_id, role):
        return jsonify({
            'response': 'error user name or pwd'
        })

    if role_in != role:
        return jsonify({
            'response': 'error role'
        })

    return jsonify({
            'response': 'success',
            'user_id': user_id,
            'user_name': user_name
        })


@app.route("/register", methods=["POST"])
def register():
    user_name = request.json.get("user_name")
    pwd = request.json.get("pwd")
    role = request.json.get("role")

    if user_name is None or pwd is None or role is None:
        msg = 'input none'
        return msg
    # user_name = re.search(r"^(?=.*[a-zA-Z])(?=.*\d).{1,10}$", user_name)
    # pwd = re.search(r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@#$%^&+=!])(?!.*\s).{1,10}$", pwd)
    if user_name is None or pwd is None:
        msg = 'input illegal'
        return msg

    if role not in ('admin', 'employee', 'customer'):
        msg = 'illegal role'
        return msg

    user_id = add_account(user_name, pwd, role)

    if user_id is None:
        msg = 'fail to register'
        return msg

    return flask.render_template('login.html')


@app.route('/account_list')
def get_account_list():
    account_list = db.get_account_list()
    return jsonify({
        'account_list': account_list
    })


@app.route('/del_account')
def del_account():
    user_id = request.args.get('user_id')
    res = db.del_account_admin(user_id)
    if res is None:
        return jsonify({
            'response': 'database false'
        })
    elif res:
        return jsonify({
            'response': 'success'
        })
    else:
        return jsonify({
            'response': 'false'
        })
