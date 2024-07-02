from app import app
from flask import request, jsonify
from dbse import *


@app.route("/add_check_in", methods=["POST"])
def add_check_in():
    user_id = request.json.get("user_id")
    check_in_state = request.json.get("check_in_state")
    check_time = request.json.get("check_time")
    if None in (user_id, check_in_state, check_time):
        return jsonify({
            'response': 'input none',
        })

    res = check_in.add_check_in(user_id, check_in_state, check_time)
    if res is None:
        return jsonify({
            'response': '500',
        })
    elif res == 0:
        return jsonify({
            'response': 'same name'
        })
    else:
        return jsonify({
            'response': 'success',
        })


@app.route("/del_check_in", methods=["POST"])
def del_check_in():
    check_in_id = request.json.get("check_in_id")
    if not check_in_id:
        return jsonify({
            'response': 'input none',
        })

    res = check_in.del_check_in(check_in_id)
    if res is None:
        return jsonify({
            'response': '500',
        })
    elif res == 0:
        return jsonify({
            'response': 'same name'
        })
    else:
        return jsonify({
            'response': 'success',
        })


@app.route("/change_check_in", methods=["POST"])
def change_check_in():
    check_in_id = request.json.get("check_in_id")
    user_id = request.json.get("user_id")
    check_in_state = request.json.get("check_in_state")
    check_time = request.json.get("check_time")
    if None in (user_id, check_in_state, check_time):
        return jsonify({
            'response': 'input none',
        })
    if user_id is None and check_in_state is None and check_time is None:
        return jsonify({
            'response': 'input none',
        })

    res = check_in.change_check_in(check_in_id, user_id, check_in_state, check_time)
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


@app.route("/search_check_in", methods=["POST"])
def search_check_in():
    check_in_id = request.json.get("check_in_id")
    user_id = request.json.get("user_id")
    check_in_state = request.json.get("check_in_state")
    check_time = request.json.get("check_time")
    res = check_in.search_check_in(check_in_id, user_id, check_in_state, check_time)
    if res is None:
        return jsonify({
            'response': '500',
        })

    resp = {
        'check_in_list': [{
            'check_in_id': re[0],
            'user_id': re[1],
            'check_in_state': re[2],
            'check_time': re[3],
            'real_name': employee_info.search_employee_info(re[0])[0][1],
        } for re in res]
    }
    return resp

