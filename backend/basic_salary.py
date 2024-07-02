
from app import app
from flask import request, jsonify
from dbse import *


@app.route("/change_basic_salary", methods=["POST"])
def change_basic_salary():
    role_name = request.json.get("role_name")
    role_salary = request.json.get("role_salary")
    res = basic_salary.change_basic_salary(role_name, role_salary)
    if res is None:
        return jsonify({
            'response': '500',
        })
    elif res == 0:
        return jsonify({
            'response': 'failure'
        })
    else:
        return jsonify({
            'response': 'success'
        })


@app.route("/search_basic_salary", methods=["POST"])
def search_basic_salary():
    role_name = request.json.get("role_name")
    role_salary = request.json.get("role_salary")

    res = basic_salary.search_basic_salary(role_name, role_salary)
    if res is None:
        return jsonify({
            'response': '500',
        })

    resp = {
        'basic_salary': {
            f'{re[0]}': re[1]
            for re in res}
    }
    return jsonify(resp)
